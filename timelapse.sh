#!/bin/sh
# Time-lapse capture script
# original from Andy Ibbitson 17-03-2013
# modified Andy Seubert 2013/05/24
###############################

cam="counter"
# make a directory for today
foldername=$(date +%Y%m%d)
mkdir -p /var/www/timelapse/$foldername/counter
mkdir -p /var/www/timelapse/$foldername/door
i=0
while :
do
echo "CAPTURING... [CTRL+C] to cancel..."
while [ $i -lt 3600 ]
	do 
		filedate=$(date +"%Y%0j%0H%0I%M%S")
		cam="counter"
		fswebcam -q -r 960x720 --font /usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf -d /dev/video0 -p MJPEG --save /var/www/timelapse/$foldername/$cam/$filedate.jpg >/dev/null 2>&1
		cam="door"
		fswebcam -q -r 960x720 --font /usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf -d /dev/video1 -p MJPEG --save /var/www/timelapse/$foldername/$cam/$filedate.jpg >/dev/null 2>&1

		sleep 0.5
		i=$(($i+1))
	done
  

moviedate=$(date +"%F-%H-%M")
cam="counter"
mencoder -nosound -mf fps=1 -o /var/www/timelapse/movies/$cam\_$moviedate.avi -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=8000 mf:///var/www/timelapse/$foldername/$cam/\*.jpg
cam="door"
mencoder -nosound -mf fps=1 -o /var/www/timelapse/movies/$cam\_$moviedate.avi -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=8000 mf:///var/www/timelapse/$foldername/$cam/\*.jpg

## upload to docs
cam="counter"
/root/uploader.py /root/uploader.cfg /var/www/timelapse/movies/$cam\_$moviedate.avi &
cam="door"
/root/uploader.py /root/uploader.cfg /var/www/timelapse/movies/$cam\_$moviedate.avi &

## find images older than 90 minutes and delete them from the snapshot folder
done