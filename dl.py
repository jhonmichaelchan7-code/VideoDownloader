import yt_dlp
import sys
import os
import signal
import glob
from datetime import timedelta

# Video URL
video_url = ""

# Global variable to track output file
output_file = None

# Cleanup leftover partial files
def cleanup_partial():
    for file in glob.glob("*.part") + glob.glob("*.ytdl"):
        try:
            os.remove(file)
            print(f"Deleted leftover file: {file}")
        except:
            pass

# Progress hook with dynamic bar, speed, ETA, total size
def progress_hook(d):
    global output_file
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        output_file = d.get('filename', None)
        if total:
            percent = downloaded / total * 100
            bar_length = 30
            filled_length = int(bar_length * downloaded // total)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)
            sys.stdout.write(
                f"\r|{bar}| {percent:.2f}% "
                f"{downloaded/1024/1024:.2f}MB/{total/1024/1024:.2f}MB "
                f"Speed: {speed/1024:.2f} KB/s "
                f"ETA: {str(timedelta(seconds=eta))}"
            )
            sys.stdout.flush()
    elif d['status'] == 'finished':
        print("\nDownload finished, now processing...")

# Handle Ctrl+C safely
def signal_handler(sig, frame):
    print("\nDownload interrupted!")
    if output_file and os.path.exists(output_file):
        os.remove(output_file)
        print(f"Partial file '{output_file}' deleted.")
    cleanup_partial()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# yt-dlp options (Windows-friendly)
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'progress_hooks': [progress_hook],
    'merge_output_format': 'mp4',
    'hls_prefer_native': False,  # Use ffmpeg to handle HLS streams
    'noplaylist': True,          # Prevent playlists
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        print("\nSuccessfully downloaded!")
except Exception as e:
    print(f"\nCould not download video: {e}")
    if output_file and os.path.exists(output_file):
        os.remove(output_file)
        print(f"Partial file '{output_file}' deleted due to error.")
    cleanup_partial()
