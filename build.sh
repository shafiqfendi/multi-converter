#!/usr/bin/env bash
# Script ini digunakan oleh Render untuk install library dan muat turun FFmpeg (Wajib untuk MP3)

set -o errexit

# Install Python libraries
pip install -r requirements.txt
pip install --upgrade yt-dlp

# Download dan setup fail FFmpeg static (Sebab Render tak benarkan sudo apt-get)
echo "Downloading FFmpeg..."
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg-release-amd64-static.tar.xz

# Pindahkan file execution ffmpeg ke luar
mv ffmpeg-*-static/ffmpeg .
mv ffmpeg-*-static/ffprobe .

# Buang folder zip yang dah tak guna untuk jimat space
rm -rf ffmpeg-*-static ffmpeg-release-amd64-static.tar.xz

echo "Build berjaya!"