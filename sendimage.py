#!/usr/bin/python

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import argparse

## default vars
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
 
strFrom = 'you@you.com'
password = "password"
strTo = 'you@you.com'
subject = 'photo from you'
message = 'Images attached. \n 0_0'
 
directory = "/var/www/"
 
#arguments sent
parser = argparse.ArgumentParser(description='send an email with attachment')
#parser.add_argument('-u','--username', help='username to auth with gmail with', required=True)
#parser.add_argument('-p','--password', help='password  to auth with gmail with', required=True)
#parser.add_argument('-s','--subject', help='subject of email', required=True)
#parser.add_argument('-b','--body', help='body text of email', required=True)
parser.add_argument('-a','--attach', help='full path to filename to attach', required=True)
args = vars(parser.parse_args())

#sender = args['username']
#password = args['password']
#subject = args['subject']
#message = args['body']
#directory = args['attach'].lstrip()
attachmentimg=args['attach'].lstrip()

# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = subject
msgRoot['From'] = strFrom
msgRoot['To'] = strTo
msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# We reference the image in the IMG SRC attribute by the ID we give it below
msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
msgAlternative.attach(msgText)

# open the file
fp = open(attachmentimg, 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage)

# Send the email (this example assumes SMTP authentication is required)
import smtplib
session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
 
session.ehlo()
session.starttls()
session.ehlo
session.login(strFrom, password)
 
session.sendmail(strFrom, strTo, msgRoot.as_string())
session.quit()
 
