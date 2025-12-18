# Video Downloader using yt-dlp

A Python script to download videos from HLS/m3u8 streams with a dynamic progress bar and automatic cleanup of partial files.

## Features
- Downloads best video + audio and merges into MP4
- Dynamic console progress bar with percentage, speed, ETA, and size
- Auto-deletes partial files if interrupted (Ctrl+C) or failed
- Works with HLS/m3u8 streams using ffmpeg

## Requirements
- Python 3.14+
- yt-dlp
- ffmpeg

## Installation
1. Install Python and add it to PATH.
2. Install required packages:
```
pip install yt-dlp
```
3. Install ffmpeg and add `ffmpeg\bin` to PATH.

## Usage
```
python dl.py
```

Press Ctrl+C to stop; partial files will be automatically deleted.
