import sys
import time
import math
import schedule
import argparse
import datetime as dt
import subprocess as sp
from server import Server


# global vars
global frame_no
global term_frame


def set_led_trigger(mode):
    sp.Popen('echo ' + mode + ' | sudo tee /sys/class/leds/led0/trigger', shell='True', stdout=sp.DEVNULL)  # green led
    sp.Popen('echo ' + mode + ' | sudo tee /sys/class/leds/led1/trigger', shell='True', stdout=sp.DEVNULL)  # red led


def set_led(ledc, status):
    led        = '0' if ledc == 'green' else '1'
    brightness = '0' if status == 'off' else '1'

    sp.Popen('echo ' + brightness + ' | sudo tee /sys/class/leds/led' + led + '/brightness', shell=True, stdout=sp.DEVNULL)


def take_picture():
    """Takes a picture and pipes it into the stdin of the ffmpeg process"""
    global frame_no
    try:

        if not args.no_led:
            # turn on green led to indicate activity
            set_led('green', 'on')

        raspistill = sp.Popen(['raspistill', '-t', '1000',
                               '-rot', '180',
                               '-w', '1920',
                               '-h', '1080',
                               '-o', 'current.jpg'])

        try:
            outs1, errs1 = raspistill.communicate(timeout=1000)
            cat = sp.Popen(['cat', 'current.jpg'], stdout=ffmpeg.stdin)
            outs, errs = cat.communicate(timeout=1000)
            if errs is not None or errs1 is not None:
                print(outs, errs)
                print('Error detected')
                if not args.no_led:
                    set_led('red', 'on')

        except:
            raspistill.kill()
            outs, errs = raspistill.communicate()
            print(outs, errs)
            print('Timeout encountered')
            if not args.no_led:
                set_led('red', 'on')

        if not args.no_led:
            # deactivate green led to indicate no activity
            set_led('green', 'off')

        frame_no += 1  # increment frame count
        sys.stdout.write('\rFrame: %i' % frame_no)
        sys.stdout.flush()
        if frame_no == term_frame:
            return schedule.CancelJob

    except:
        print('Something happend')


def cleanup():
    """Performs cleanup actions"""
    print()
    print('Stopping timelapse...')
    ffmpeg.stdin.close()
    print('Finishing encoding...')
    ffmpeg.communicate()
    print('Resetting led configuration')
    set_led_trigger('input')

    for job in schedule.jobs:
        schedule.cancel_job(job)

    print('Timelapse finished')


# MAIN #
# create cli argument parser
parser = argparse.ArgumentParser(
    description='Records a timelapse video using the raspberry\'s camera module. Use ^C to stop recording.')
parser.add_argument('-i', type=int, default=5, dest='interval',
                    help='Set the interval in which to take photos in seconds.')
parser.add_argument('-d', type=int, default=0, dest='duration',
                    help='Set the duration for which the timelapse should record in minutes, 0 for endless.')
parser.add_argument('-o', type=str, dest='out_name',
                    default='./timelapse' + dt.datetime.now().strftime("%Y%m%d_%H%M%S") + '.mp4',
                    help='Set the output file name.')
parser.add_argument('--no-led', action='store_true')
parser.add_argument('--no-server', action='store_true')
args = parser.parse_args()

if not args.no_led:
    # switch pi leds to manual mode
    set_led_trigger('gpio')

    # turn off all pi leds to indicate no problem and no activity
    set_led('red', 'off')
    set_led('green', 'off')

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

if not args.no_server:
    print('Starting webserver')
    server = Server()
    server.start()

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
