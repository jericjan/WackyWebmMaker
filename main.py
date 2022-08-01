"""
Wacky Webm Maker
    For making those funny discord videos that magically change screen resolution.
"""

import os
import subprocess
import sys
import shutil

from PIL import Image

print("What is your folder location of PNGs?")
folder = input()
folder = folder.strip("\"'")
print("What is your original vid file location?")
og_vid = input()
og_vid = og_vid.strip("\"'")


print("")

files = os.listdir(folder)
files = [os.path.join(folder, x) for x in files]
not_images = [x for x in files if not x.lower().endswith(("png", "jpg", "jpeg"))]
while len(not_images) > 0:
    nl = "\n"
    print(
        f"Found {len(not_images)} Non-image files!\n"
        f"{nl.join(not_images)}\n"
        f"Please delete or move them somewhere else and press ENTER to continue"
    )
    input()
    files = os.listdir(folder)
    files = [os.path.join(folder, x) for x in files]
    not_images = [x for x in files if not x.lower().endswith(("png", "jpg", "jpeg"))]

for i in files:
    print(f"Cropping {os.path.basename(i)}...")
    im = Image.open(i)
    if im.size != im.getbbox():
        im2 = im.crop(im.getbbox())
        im2.save(i)
print("Finished cropping all images!\n")


coms = [
    "ffprobe",
    "-v",
    "0",
    "-of",
    "csv=p=0",
    "-select_streams",
    "v:0",
    "-show_entries",
    "stream=r_frame_rate",
    og_vid,
]
try:
    with subprocess.Popen(
        coms, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as process:
        stdout, stderr = process.communicate()
except FileNotFoundError as e:
    print(
        f"{e}\n\nYou probably don't have ffprobe installed or in the same folder as this program"
    )
    sys.exit()
stdout = stdout.decode("utf-8")
fps_num = stdout.split("/")[0]
fps_den = stdout.split("/")[1]
framerate = int(fps_num) / int(fps_den)
print(f"Video is {framerate} FPS\n")
temp_folder = os.path.join(folder, "temp")
if not os.path.exists(temp_folder):
    os.mkdir(temp_folder)
files = os.listdir(folder)
files = [os.path.join(folder, x) for x in files]
for file in files:
    if file != "temp":
        filename = os.path.splitext(os.path.basename(file))[0]
        webm_file = os.path.join(temp_folder, f"{filename}.webm")
        print(f"Converting {filename} to WEBM...")
        coms = ["ffmpeg", "-y", "-i", file, "-filter:v", f"fps={framerate}", webm_file]
        try:
            with subprocess.Popen(
                coms, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ) as process:
                stdout, stderr = process.communicate()
        except FileNotFoundError as e:
            print(
                f"{e}\n\nYou probably don't have ffmpeg installed or in the same folder as this program"
            )
            sys.exit()
        stdout, stderr = process.communicate()
print("Finished converting all images!\n")


list_file = os.path.join(temp_folder, "list.txt")
files = os.listdir(temp_folder)
files = [os.path.join(temp_folder, x) for x in files]
with open(list_file, "w", encoding="utf-8") as f:
    f.write("")
for file in files:
    with open(list_file, "a", encoding="utf-8") as f:
        if not file.endswith(("list.txt", "final.webm", "audio.opus")):
            f.write(f"file '{file}'\n")

print("Combining WEBMs...\n")
concatted = os.path.join(temp_folder, "final.webm")
coms = [
    "ffmpeg",
    "-y",
    "-f",
    "concat",
    "-safe",
    "0",
    "-i",
    list_file,
    "-c",
    "copy",
    concatted,
]
with subprocess.Popen(coms, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
    stdout, stderr = process.communicate()


print("Extracting audio from OG video...\n")
opus_audio = os.path.join(temp_folder, "audio.opus")
coms = ["ffmpeg", "-y", "-i", og_vid, opus_audio]
with subprocess.Popen(coms, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
    stdout, stderr = process.communicate()


print("Adding audio to WEBM...\n")
final_file = os.path.join(folder, "final.webm")
coms = [
    "ffmpeg",
    "-y",
    "-i",
    concatted,
    "-i",
    opus_audio,
    "-map",
    "0:v:0",
    "-map",
    "1:a:0",
    "-c",
    "copy",
    final_file,
]

with subprocess.Popen(coms, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
    stdout, stderr = process.communicate()
shutil.rmtree(temp_folder)

print(f"DONE!\n" f"Your file is in {final_file}\n" f"Enjoy!")
