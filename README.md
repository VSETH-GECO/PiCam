# PiCam

## Setup
* Install pip and ffmpeg with `apt install pip3 ffmpeg` (may need sudo)
* Install schedule module with `pip3 install schedule`

## Usage
Run with `python3 timelapse.py`  
Get help by running `python3 timelapse.py --help`

Advanced use:  
`-i number` to set the interval between the pictures to the number in seconds. Default 5, not recommended to use < 3.  
`-d number` to set the duration for which the timelapse should run before stopping automatically. Default 0, no auto stop.  
`-o str` to set the name of the output file. Default is timelapse`date_time`.mp4

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
necessary for playback.