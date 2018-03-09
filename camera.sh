#!/bin/bash

# check if pi cam is enabled
if [ grep "start_x" /boot/config.txt ]; then
    if [ grep "start_x=1" /boot/config.txt ]; then
	echo "Camera already enabled, proceeding."
    else
        echo "Enabling camera..."
        # enable camera

        sed -i "s/start_x=0/start_x=1/g" /boot/config.txt

	echo "Camera enabled, reboot now please."
    	return 0
    fi
fi

# mount remote fs to store pictures
read -p 'IP/name of nas server: ' nasip
echo "Mounting nfs..."

sudo mount -t nfs -o soft ${nasip}:/mnt/RAID1/backup /home/pi/nfs
echo "Nfs mounted"

# set capture interval and start camera
read -p 'Capture interval in ms (default 5000): ' capinterval
echo "Beginning timelapse recording..."
raspistill -w 1920 -h 1080 -t 0  -tl ${capinterval:-5000} -o /home/pi/nfs/pi-cam/timelapse_%08d.jpg
