from PIL import Image
import os
import math

print("What is your folder location?")
folder = input()
print("Start at what frame?")
start_frame = input()
print("End at what frame?")
end_frame = input()
num_frames = int(end_frame) - int(start_frame) + 1
print(f"{num_frames} frames!")
path = os.path.join(folder, f"{start_frame}.png")
im = Image.open(path)
width = im.size[0]
height = im.size[1]
print(f"Image is w:{width} h:{height}")
decrement = (width - 1) / (int(num_frames) - 1)
print(f"for every frame, you should decrease the width by {decrement}")
resize_list = []
for x in range(num_frames):
    position = int(start_frame) + x
    new_width = round(width - (decrement * x))
    new_height = math.ceil(height * new_width / width)
    print(f"{position}: {new_width} x {new_height}")
    newsize = (new_width, new_height)
    path = os.path.join(folder, f"{position:04}.png")
    im = Image.open(path)
    im = im.resize(newsize)
    im.save(path)
    # resize_list.append((new_width,new_height))

# print(resize_list)
