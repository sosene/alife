@echo off
ffmpeg -f image2 -i oaa_1_%%d.png -vcodec mpeg4 -b:v 3200k video_.avi
ffmpeg -i video_.avi -pix_fmt rgb24 out_.gif
