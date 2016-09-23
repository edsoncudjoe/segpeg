#!/usr/bin/env python2.7

import argparse
import glob
import os
import shutil
import subprocess

# Users need to be able to define
# Output directory
# Segment size
# Video quality out of defined presets : proxy, iphone, web, android


# Basic Settings
FFMPEG = '/usr/local/bin/ffmpeg'
CRF_VALUE = '25'
VIDEO_BR = '100' + 'k'
AUDIO_BR = '96' + 'k'
PRESET = 'ultrafast'

TEMP_DIR = os.path.expanduser('~/Segpeg/tmp')
OUT_DIR = os.path.expanduser('~/Segpeg/out')

# Temp files go here
tmpf = TEMP_DIR


# Input file
#inpf = '/Users/Admin/Movies/sample media files/_BBC Motion Gallery.mov'

parser = argparse.ArgumentParser(description='Another proxy file creator')
parser.add_argument('-i', '--input', help='select the source file.')
#parser.add_argument('-o', '--output', help='select output directory')

arg = parser.parse_args()

if arg.input:
    inpf = arg.input
    if inpf[-1] == '/':
        inpf = inpf[:-1]





# Segments need to be limited between 1 and 120 seconds
segment_size = '30'



# segment file command
segment_file = [
    FFMPEG, '-i', inpf,
    '-acodec', 'copy',
    '-f', 'segment',
    '-segment_time', segment_size,
    '-vcodec', 'copy',
    '-reset_timestamps', '1',
    '-map', '0',
    '{}/segment_%d.mp4'.format(tmpf)
]

if __name__ == '__main__':
    # Build temp file
    if os.path.isdir(tmpf):
        print('\ntemp file created')
        pass
    else:
        print tmpf
        os.makedirs(tmpf)
    
    
    # Segment file
    print('\nBuilding segments...')
    a = subprocess.Popen(segment_file, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    output, errors = a.communicate()
    
    
    
    # Convert segments
    print('\nConverting segments please wait.')
    cnvt = subprocess.Popen(['/Users/Admin/scripts/ffmpeg_/proxy_gen.sh',
                             tmpf, tmpf],
                            stdout=subprocess.PIPE)
    output = cnvt.communicate()
    
    
    # Join converted segments
    print('\nJoining converted segments...')
    concat = subprocess.Popen([
            FFMPEG,
            '-f', 'concat',
            '-i', '{}/{}/output.txt'.format(tmpf, tmpf),
            '-c', 'copy',
            '/Users/Admin/Movies/sample media files/segmented_output.mp4'
            ], stdout=subprocess.PIPE)
    cct_out = concat.communicate()
    
    # Deleted tmp contents
    shutil.rmtree(tmpf)
    print('\nProxy conversion complete.')