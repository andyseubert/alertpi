#!/usr/bin/python
import time
from time import sleep
import datetime
import os
import sys
import shlex
import subprocess
from subprocess import Popen


when = datetime.datetime.now().strftime('%B%d-%H%M%S')

## take photos
photodir="/var/www/"
archivedir="/var/www/timelapse/"
## move files from photodir to archivedir
try:
    os.rename (photodir+"countercam.jpg",archivedir+when+"countercam.jpg")
    os.rename (photodir+"doorcam.jpg",archivedir+when+"doorcam.jpg")
except:
   print 'Oh well..'

### set up commands
counterimg=photodir+"countercam.jpg"
countercam="/dev/video0"
countercmd="/usr/bin/fswebcam -q -r 960x720 --font /usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf -d "+countercam+" "+counterimg

doorimg=photodir+"doorcam.jpg"
doorcam="/dev/video1"
doorcmd="/usr/bin/fswebcam -q -r 960x720 --font /usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf -d "+doorcam+" "+doorimg

cmd=shlex.split(countercmd)
try:
    subprocess.Popen(cmd)
except:
    print "error running ".countercmd
print ("just took counter snapshot success?")

cmd=shlex.split(doorcmd)
subprocess.Popen(cmd)

print ("just took door snapshot success?")
#print ("sleeping 5")
#sleep(10)
#print ("sending image "+counterimg)
#subprocess.Popen(["/root/sendimage.py","-a "+counterimg])
