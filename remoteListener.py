#!/usr/bin/python
from time import sleep
import os
import sys
import subprocess
from subprocess import Popen
import RPi.GPIO as GPIO

# global variables for commands and status
global alertcmd
global alarmOn
# the alertcmd should be slightly different depending on which event triggers it (button or remote)
# because later we can add conditions for doors or other x10 devices
alertcmd = "/root/testalert.py" 
# inital alarm status is off
alarmOn  = False
status = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN) # RF receiver
GPIO.setup(2, GPIO.IN)  # Front push button
GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH) # green led starts ON
GPIO.setup(9, GPIO.OUT, initial=GPIO.LOW)   # red led starts OFF

def alert_action(channel):
	from time import sleep
	global alertcmd
	global alarmOn
	global status
	
	print('Edge detected on channel %s'%channel)
		
	#if channel == 17 : alertcmd = "/root/rfalert.py"
	if channel == 2 :
		alertcmd = "/root/pushAlert.py"
		if alarmOn==True: 
			status = "0"
			subprocess.Popen([sys.executable, alertcmd, status])
			alarmOn=False	
			GPIO.output(11,GPIO.HIGH) ## turn green led on
			GPIO.output(9,GPIO.LOW)   ## turn red led off
			print ('Alarm was On now it is Off')	
		else:
			status = "1"
			subprocess.Popen([sys.executable, alertcmd, status])
			alarmOn=True
			GPIO.output(9,GPIO.HIGH) ## turn red LED on
			GPIO.output(11,GPIO.LOW) ## turn green LED off
			print ('Alarm was OFF now it is ON')
	if channel == 17 : 
		alertcmd = "/root/rfalert.py"
		status = "0"
		subprocess.Popen([sys.executable, alertcmd, status])
		
print ("READY")


GPIO.add_event_detect(17, GPIO.RISING, callback=alert_action, bouncetime=200)
GPIO.add_event_detect(2, GPIO.FALLING, callback=alert_action, bouncetime=200) 



while True:
	sleep(1)
	
	
GPIO.cleanup()
