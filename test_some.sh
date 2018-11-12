#!/bin/bash
# to get rid of MSDOS format do this to this file: sudo sed -i s/\\r//g ./filename
# or, open in nano, control-o and then then alt-M a few times to toggle msdos format off and then save

rm ./0.debug.log

./cross_compiler.py -p ffmpeg_static_non_free 2>&1 | tee -a ./0.debug.log
read -p "done.  press enter to continue"
./cross_compiler.py -p ffmpeg_static_non_free_opencl 2>&1 | tee -a ./0.debug.log
read -p "done.  press enter to continue"
./cross_compiler.py -p x264 2>&1 | tee -a ./0.debug.log
read -p "done.  press enter to continue"
./cross_compiler.py -p x265_multibit 2>&1 | tee -a ./0.debug.log
read -p "done.  press enter to continue"
./cross_compiler.py -p mp4box 2>&1 | tee -a ./0.debug.log
read -p "done.  press enter to continue"
./cross_compiler.py -p lame 2>&1 | tee -a ./0.debug.log
read -p "done.  press enter to continue"
./cross_compiler.py -p aom 2>&1 | tee -a ./0.debug.log
read -p "done.  press enter to continue"
./cross_compiler.py -p sox 2>&1 | tee -a ./0.debug.log
read -p "done.  press enter to continue"
./cross_compiler.py -p vpx 2>&1 | tee -a ./0.debug.log
read -p "done.  press enter to continue"
./cross_compiler.py -p mediainfo 2>&1 | tee -a ./0.debug.log
read -p "done.  press enter to continue"
./cross_compiler.py -p dav1d 2>&1 | tee -a ./0.debug.log
read -p "done.  press enter to continue"
./cross_compiler.py -p fftw3_dll 2>&1 | tee -a ./0.debug.log
read -p "done.  press enter to continue"
