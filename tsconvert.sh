#!/bin/bash
for name in *.ts; do
  ffmpeg -i "$name" -acodec copy -vcodec copy "${name%.*}.mp4" 
done 
