#converts the video to mp3

import os
import subprocess

files=os.listdir("videos")
for file in files:
    file_name=file.split("(")[0]
    # print(file_name)
    subprocess.run(["ffmpeg", "-i", f"videos/{file}", f"audios/{file_name}.mp3"])