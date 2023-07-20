import urllib.request
import io
from PIL import Image
import random
from random import sample
import math
import sys
import pickle
import time

#K = int(sys.argv[2])
#URL = sys.argv[1]
K = 8
URL = 'https://i.pinimg.com/originals/95/2a/04/952a04ea85a8d1b0134516c52198745e.jpg'
f = io.BytesIO(urllib.request.urlopen(URL).read()) # Download the picture at the url as a file object
img = Image.open(f) # You can also use this on a local file; just put the local filename in quotes in place of f; img is k-means output image
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so. 
WIDTH, HEIGHT = img.size

x = (1, 2, 3)
print(5*x)