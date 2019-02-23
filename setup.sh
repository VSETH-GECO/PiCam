#!/bin/bash

echo "Performing setup"
restart=0

# check if pi cam is enabled
if grep "start_x" /boot/config.txt ; then
    if grep "start_x=1" /boot/config.txt ; then
	    echo "Camera already enabled, proceeding."
    else
        echo "Enabling camera..."
        # enable camera

        sudo sed -i "s/start_x=0/start_x=1/g" /boot/config.txt

	    echo "Camera enabled, reboot required at the end of the setup."
    	restart=1
    fi
fi

# check if all dependencies are installed
sudo apt-get update
sudo apt-get install ffmpeg python3-pip

pip3 install schedule twisted

# setup done, inform user if restart is required
if [[ "$restart" -eq "1" ]] ; then
    echo "Setup completed. Please reboot now to finish camera setup"
else
    echo "Setup completed. Begin timelapse by running python3 timelapse.py"
fi
