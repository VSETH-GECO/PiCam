import time
import os
import schedule
import subprocess as sp


def take_picture():
    raspistill = sp.Popen(['raspistill', '-t', '1000', '-rot', '180', '-w', '1920', '-h', '1080', '-o', '-'], stdout=ffmpeg.stdin)


if os.path.isfile('./timelapse.mp4'):
    print('Old timelapse.mp4 found. Please rename/move before starting a new timelapse!')
    quit()

ffmpeg = sp.Popen(['ffmpeg', '-f', 'image2pipe', '-framerate', '25', '-i', '-', '-g', '120', '-c:v', 'libx264', '-f', 'mp4', '-movflags', 'frag_keyframe+empty_moov', '-r', '25', 'timelapse.mp4'], stdin=sp.PIPE)
schedule.every(5).seconds.do(take_picture)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print('Stopping timelapse...')
    ffmpeg.stdin.close()
    print('Timelapse finished')
