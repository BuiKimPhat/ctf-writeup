import imageio
from PIL import Image, GifImagePlugin
from Crypto.Util.number import long_to_bytes as l2b, bytes_to_long as b2l
import random
from apng import APNG

filenames = []
flag = "REDACTED" 

orig_filename = "ostrich.jpg"
orig_image = Image.open(orig_filename)
pixels = orig_image.load()
width, height = orig_image.size
images = []

for i in range(len(flag)):
    new_filename = f'./images/ostrich{i}.png'
    new_image = Image.new(orig_image.mode, orig_image.size)
    new_pixels = new_image.load()
    for x in range(width):
        for y in range(height):
            new_pixels[x,y] = orig_image.getpixel((x, y))

    x = random.randrange(0,width)
    y = random.randrange(0,height)
    pixel = list(orig_image.getpixel((x, y)))
    while(pixel[2] == 0):
        x = random.randrange(0,width)
        y = random.randrange(0,height)
        pixel = list(orig_image.getpixel((random.randrange(0,width), random.randrange(0,height))))
    
    new_val = l2b(pixel[2]*ord(flag[i]))
    pixel[0] = new_val[0]
    if len(new_val) > 1:
        pixel[1] = new_val[1]
    pixel[2] = 0

    new_pixels[x, y] = (pixel[0], pixel[1], pixel[2])
    new_image.save(new_filename)
    filenames.append(new_filename)
    images.append(new_image)

APNG.from_files(filenames, delay=0).save("result.apng")

