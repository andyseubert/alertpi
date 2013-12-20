#!/usr/bin/python
'''
Created on 6 Jun 2012

@author: Jeremy Blythe

Motion Uploader - uploads videos to Google Drive

Read the blog entry at http://jeremyblythe.blogspot.com for more information
'''

import smtplib
from datetime import datetime

import os.path
import sys
import base64

import gdata.data
import gdata.docs.data
import gdata.docs.client
import ConfigParser

class MotionUploader:
    def __init__(self, config_file_path):
        # Load config
        config = ConfigParser.ConfigParser()
        config.read(config_file_path)
        
        # GMail account credentials
        self.username = config.get('gmail', 'user')
        self.password = config.get('gmail', 'password')
        self.from_name = config.get('gmail', 'name')
        self.sender = config.get('gmail', 'sender')
        
        # Recipient email address (could be same as from_addr)
        self.recipient = config.get('gmail', 'recipient')        
        
        # Subject line for email
        self.subject = config.get('gmail', 'subject')
        
        # First line of email message
        self.message = config.get('gmail', 'message')
                
        # Folder (or collection) in Docs where you want the videos to go
        self.folder = config.get('docs', 'folder')
        
        # Options
        self.delete_after_upload = config.getboolean('options', 'delete-after-upload')
        self.send_email = config.getboolean('options', 'send-email')
        
        self._create_gdata_client()

    def _create_gdata_client(self):
        """Create a Documents List Client."""
        self.client = gdata.docs.client.DocsClient(source='motion_uploader')
        self.client.http_client.debug = False
        self.client.client_login(self.sender, self.password, service=self.client.auth_service, source=self.client.source)
               
    def _get_folder_resource(self):
        """Find and return the resource whose title matches the given folder."""
        col = None
        for resource in self.client.GetAllResources(uri='/feeds/default/private/full/-/folder'):
            if resource.title.text == self.folder:
                col = resource
                break    
        return col
    
    def _send_email(self,msg,imgpath):
        '''Send an email using the GMail account.'''
        senddate=datetime.strftime(datetime.now(), '%Y-%m-%d')
        # Read a file and encode it into base64 format
        fo = open(imgpath, "rb")
        filecontent = fo.read()
        encodedcontent = base64.b64encode(filecontent)  # base64
        imgfile=os.path.basename(imgpath)
        marker = "AUNIQUEMARKER"
        p1="Date: %s\r\nFrom: %s <%s>\r\nTo: %s\r\nSubject: %s\r\nContent-Type: multipart/mixed; boundary=%s\r\n--%s\r\n" % (senddate, self.from_name, self.sender, self.recipient, self.subject, marker, marker)
        p2="Content-Type: text/plain\r\nContent-Transfer-Encoding:8bit\r\n\r\n%s\r\n--%s\r\n" % (msg, marker)
        p3="Content-Type: multipart/mixed; name=""%s""\r\nContent-Transfer-Encoding:base64\r\nContent-Disposition: attachment; filename=%s\r\n\r\n%s\r\n--%s--\r\n" % (imgfile, imgfile, encodedcontent, marker)

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(self.sender, self.recipient, p1+p2+p3)
        server.quit()

    def _upload(self, video_file_path, folder_resource):
		'''Upload the video and return the doc'''
		doc = gdata.docs.data.Resource(type='image', title=os.path.basename(video_file_path))
		media = gdata.data.MediaSource()
		media.SetFileHandle(video_file_path, 'image/jpeg')
		#create_uri = gdata.docs.client.RESOURCE_UPLOAD_URI + '?convert=false'
		doc = self.client.CreateResource(doc, media=media, collection=folder_resource)#, create_uri=create_uri )
		return doc
    
    def upload_video(self, video_file_path):
        """Upload a video to the specified folder. Then optionally send an email and optionally delete the local file."""
        folder_resource = self._get_folder_resource()
        if not folder_resource:
            raise Exception('Could not find the %s folder' % self.folder)

        doc = self._upload(video_file_path, folder_resource)
                      
        if self.send_email:
            video_link = None
            for link in doc.link:
                if 'docs.google.com' in link.href:
                    video_link = link.href
                    break
            # Send an email with the link if found
            msg = self.message
            if video_link:
                msg += '\n\n' + video_link
            imgfile = os.path.splitext(video_file_path)[0] + ".jpg"
            self._send_email(msg,imgfile)

        if self.delete_after_upload:
            os.remove(video_file_path)

if __name__ == '__main__':         
    try:
        if len(sys.argv) < 3:
            exit('Motion Uploader - uploads videos to Google Drive\n   by Jeremy Blythe (http://jeremyblythe.blogspot.com)\n\n   Usage: uploader.py {config-file-path} {video-file-path}')
        cfg_path = sys.argv[1]
        vid_path = sys.argv[2]    
        if not os.path.exists(cfg_path):
            exit('Config file does not exist [%s]' % cfg_path)    
        if not os.path.exists(vid_path):
            exit('file does not exist [%s]' % vid_path)    
        MotionUploader(cfg_path).upload_video(vid_path)        
    except gdata.client.BadAuthentication:
        exit('Invalid user credentials given.')
    except gdata.client.Error:
        exit('Login Error')
    except Exception as e:
        exit('Error: [%s]' % e)
