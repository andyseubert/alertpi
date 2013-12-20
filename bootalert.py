#!/usr/bin/python
import time
from time import sleep
import datetime
import os
import sys
import subprocess
from subprocess import Popen
import pynma
p = pynma.PyNMA( "12842c4d5f6061eb9543674248c3518edda9dd83343ebe19" )
application="alertpi boot"
event="alertpiOnBoot"
description="alertpi just turned on"
priority=2

snap1cmd="fswebcam -q --no-banner -r 960x720 -d /dev/video0 /var/www/countercam.jpg"
snap2cmd="fswebcam -q --no-banner -r 960x720 -d /dev/video1 /var/www/doorcam.jpg"

subprocess.Popen([sys.executable, snap1cmd ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
subprocess.Popen([sys.executable, snap2cmd ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
p.push(application, event, description)
subprocess.Popen([sys.executable, "/root/sendsms.py BootedUpJustNow" ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)


