import sys
import time
import math
import schedule
import argparse
import datetime as dt
import subprocess as sp


# global vars
global frame_no
global term_frame


def take_picture():
    """Takes a picture and pipes it into the stdin of the ffmpeg process"""
    global frame_no

    #raspistill = sp.Popen(['raspistill', '-t', '1000',
    #                       '-rot', '180',
    #                       '-w', '1920',
    #                       '-h', '1080',
    #                       '-o', '-'], stdout=ffmpeg.stdin)
    frame_no += 1  # increment frame count
    sys.stdout.write('\rFrame: %i' % frame_no)
    sys.stdout.flush()
    if frame_no == term_frame:
        return schedule.CancelJob


def cleanup():
    """Performs cleanup actions"""
    print()
    print('Stopping timelapse...')
    ffmpeg.stdin.close()
    print('Finishing encoding...')
    ffmpeg.communicate()
    print('Timelapse finished')


# MAIN #
# create cli argument parser
parser = argparse.ArgumentParser(
    description='Records a timelapse video using the raspberry\'s camera module. Use ^C to stop recording.')
parser.add_argument('-i', type=int, default=5, dest='interval',
                    help='Set the interval in which to take photos in seconds.')
parser.add_argument('-t', type=int, default=0, dest='duration',
                    help='Set the duration for which the timlapse should record in minutes, 0 for endless.')
parser.add_argument('-o', type=str, dest='out_name',
                    default='./timelapse' + dt.datetime.now().strftime("%Y%m%d_%H%M%S") + '.mp4',
                    help='Set the output file name.')
args = parser.parse_args()

# starts a ffmpeg process that takes it's input from the stdin pipe and
# efficiently converts it into a h.264 encoded mp4 video
ffmpeg = sp.Popen(['ffmpeg', '-f', 'image2pipe',
                   '-framerate', '25',
                   '-i', '-',
                   '-g', '120',
                   '-c:v', 'libx264',
                   '-f', 'mp4',
                   '-movflags', 'frag_keyframe+empty_moov',
                   '-r', '25',
                   args.out_name],
                  stdin=sp.PIPE,
                  stdout=sp.DEVNULL,
                  stderr=sp.DEVNULL)

# calculate how many frames are needed to get to the specified end time
frame_no = 0
term_frame = math.trunc(args.duration * 60 / args.interval)

# schedule the images to be taken in the specified interval
schedule.every(args.interval).seconds.do(take_picture)
print('Started timelapse with interval=' + str(args.interval) + 's')
print('Writing to file ' + args.out_name)

try:
    running = True
    while running:
        schedule.run_pending()
        if not schedule.jobs:
            running = False
        time.sleep(1)

    cleanup()

except KeyboardInterrupt:
    cleanup()
