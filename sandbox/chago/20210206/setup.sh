#!/bin/sh

sudo add-apt-repository -y ppa:obsproject/obs-studio

sudo apt -y update
sudo apt -y upgrade
sudo apt-get -y update

sudo apt install -y ubuntu-drivers-common

sudo apt install -y nvidia-driver-460
sudo apt-get install -y ocl-icd-libopencl1 opencl-headers clinfo

sudo apt-get -y install obs-studio ffmpeg

sudo apt -y install ubuntu-desktop
sudo apt -y install xrdp


