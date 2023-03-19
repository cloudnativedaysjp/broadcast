#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Talk IDを引数で指定してください" 1>&2
  exit 1
fi

ID=$1
mkdir -p $1

echo "Generate playlist.."
echo "#EXTM3U
#EXT-X-STREAM-INF:BANDWIDTH=128000,RESOLUTION=640x360
360_out.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=200000,RESOLUTION=854x480
480_out.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=350000,RESOLUTION=1280x720
720_out.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=512000,RESOLUTION=1920x1080
1080_out.m3u8
" > ./$1/playlist.m3u8
echo "done"

echo "Start converting to 360p"
ffmpeg -i $1.mp4 \
-vcodec libx264 \
-movflags faststart \
-acodec aac \
-strict experimental \
-b:a 40.4k \
-ar 44100 \
-map 0 \
-flags +loop-global_header \
-profile:v baseline  \
-level 3.0 \
-s 640x360 \
-g 150 \
-b:v 128k \
-start_number 0 \
-hls_time 10  \
-hls_list_size 0  \
-f hls  \
./$1/360_out.m3u8
echo "done"

echo "Start converting to 480p"
ffmpeg -i $1.mp4 \
-vcodec libx264 \
-movflags faststart \
-acodec aac \
-strict experimental \
-b:a 63.4k \
-ar 44100 \
-map 0 \
-flags +loop-global_header \
-profile:v baseline  \
-level 3.0 \
-s 800x480 \
-g 150 \
-b:v 200k \
-start_number 0 \
-hls_time 10  \
-hls_list_size 0  \
-f hls  \
./$1/480_out.m3u8
echo "done"

echo "Start converting to 720p"
ffmpeg -i $1.mp4 \
-vcodec libx264 \
-movflags faststart \
-acodec aac \
-strict experimental \
-b:a 63.4k \
-ar 44100 \
-map 0 \
-flags +loop-global_header \
-profile:v baseline  \
-level 3.0 \
-s 1280x720 \
-g 150 \
-b:v 350k \
-start_number 0 \
-hls_time 10  \
-hls_list_size 0  \
-f hls  \
./$1/720_out.m3u8

echo "done"

echo "Start converting to 1080p"

ffmpeg -i $1.mp4 \
-vcodec libx264 \
-movflags faststart \
-acodec aac \
-strict experimental \
-b:a 63.4k \
-ar 44100 \
-map 0 \
-flags +loop-global_header \
-profile:v baseline  \
-level 3.0 \
-s 1920x1080 \
-g 150 \
-b:v 512k \
-start_number 0 \
-hls_time 10  \
-hls_list_size 0  \
-f hls  \
./$1/1080_out.m3u8
echo "Export finished"
