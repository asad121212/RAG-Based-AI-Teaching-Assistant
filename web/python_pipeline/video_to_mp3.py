#converts the video to mp3

import subprocess
import sys
import os

def convert_video_to_mp3(video_path, output_mp3_path):
    try:
        subprocess.run([
            "ffmpeg",
            "-y",  # overwrite output
            "-i", video_path,
            output_mp3_path
        ], check=True)
        print("MP3 conversion complete.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    video_path = sys.argv[1]
    output_mp3_path = sys.argv[2]
    convert_video_to_mp3(video_path, output_mp3_path)
