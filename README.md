# PiCam

## Setup
* Install pip and ffmpeg with `apt install pip3 ffmpeg` (may need sudo)
* Install schedule module with `pip3 install schedule`

## Usage
Run with `python3 timelapse.py`  
Run in background with `python3 timelapse.py & && disown`
Get help by running `python3 timelapse.py --help`

#### LEDs
The timelapse program will take over the red and green status LEDs of the Raspberry to indicate it's own status. As long as everything is fine both LEDs will be off with the green lighting up when a picture is taken. When any error occurs the red LED will show and it't probably a good Idea to ssh into the Raspberry and check on the process.

#### Server
The timelapse program will start a lightweight webserver on port 8080 that will show the last picture taken by the camera. This could be usefull for setting up the Pi or occasionally checking up on the status.

Advanced use:  
`-i number` to set the interval between the pictures to the number in seconds. Default 5, not recommended to use < 3.  
`-d number` to set the duration for which the timelapse should run before stopping automatically. Default 0, no auto stop.  
`-o str` to set the name of the output file. Default is timelapse`date_time`.mp4  
`--no-led` to disable the manipulation of the two status LEDs of the Pi by the program to show it's own status.  
`--no-server` to disable the webserver running on port 8080 that shows the last picture taken.  

## About
This project was developed by me as we wanted to record our lan party including setup and cleanup whithout having to
care about the devices recording the timelapse. It stores all the pictures taken in a H.264
encoded mp4 video to save as much space as possible. It could run at a 5 second interval for about 120 days
while taking up 64GB of space to do so, depending on how much changes between
each frame.  
Also you don't want your video to be corrupted if the power goes out. Because of this
the program writes 120-frame-chunks with their own metadata so you can only lose the
last <120 frames at any given time. This may create a incorrect display of timecodes
on some players so I recommend to re-encode the video after completion but it's not
necessary for playback. You can easily re-encode a video with `ffmpeg -i input.mp4 -c copy output.mp4`.
