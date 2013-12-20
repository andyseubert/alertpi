#!/usr/bin/python
import time
from time import sleep
import datetime
import os
import sys
import shlex
import subprocess
from subprocess import Popen
import pynma
p = pynma.PyNMA( "<YOURPYNMAKEYHERE>" )
application="<YOURAPPLICATIONNAME>"
when = datetime.datetime.now().strftime('%B%d-%H%M%S')

state = str(sys.argv[1])
print ("state is " + state)

if state == "1" : # alert
	event       = "Remote Triggered at "+when
	description = "DESCRIPTION"
	priority    = "-2"
if state == "0" : # alert cleared
	event       = "Remote Trigger Cleared at "+when
	description = "All Clear"
	priority    = "-2"

print (event)
## notify my android 
#p.push(application, event, description)

## send SMS alert
smscmd="/root/sendsms.py"
#subprocess.Popen([sys.executable, smscmd,event])



## take photos
photodir="/var/www/"

### set up commands
counterimg=photodir+"countercam.jpg"
countercam="/dev/video0"
countercmd="/usr/bin/fswebcam -q -r 960x720 --font /usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf -d "+countercam+" "+counterimg

doorimg=photodir+"doorcam.jpg"
doorcam="/dev/video1"
doorcmd="/usr/bin/fswebcam -q -r 960x720 --font /usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf -d "+doorcam+" "+doorimg

cmd=shlex.split(countercmd)
subprocess.Popen(cmd)
print ("just took counter snapshot success?")

cmd=shlex.split(doorcmd)
subprocess.Popen(cmd)
print ("just took door snapshot success?")

sleep(1)
subprocess.Popen("/root/snapshot.py")


emailuser="-u you@you.com"    
emailpass="-p <YOURPASSWORD>"
emailsubj="-s \""+ event +"\""
emailatt="-a /var/www/"
emailbody="-b \"" + event +"\""


#subprocess.Popen([sys.executable, "/root/sendemail.py", emailuser,emailpass,emailsubj,emailatt,emailbody])
print datetime.datetime.now()

uploadcmd="/root/uploader.py /root/uploader.cfg "+doorimg
cmd=shlex.split(uploadcmd)
# subprocess.Popen(cmd)

uploadcmd="/root/uploader.py /root/uploader.cfg "+counterimg
cmd=shlex.split(uploadcmd)
# subprocess.Popen(cmd)


print ("alerts sent")
