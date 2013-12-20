#!/usr/bin/python
import smtplib
import sys
server = smtplib.SMTP( "smtp.gmail.com", 587 )
server.starttls()
server.login( 'you@yourdomain.com', '<yourpasswordhere>' )
server.sendmail( 'alertPi', '##########@vtext.com', str(sys.argv[1]) )
