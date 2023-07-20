import urllib.request
import io
from PIL import Image
import random
import math
import sys

K = int(sys.argv[2])
URL = sys.argv[1]
#K = 8
#URL = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSyObEHVIMF5dEXqJCuEqjd0r0MRiShqqBUfg:x-raw-image:///297a9c3b253f37d5e21ee9dd2e4c7575b2c14fd2057dea990ea459da8cd74d83&usqp=CAU'
f = io.BytesIO(urllib.request.urlopen(URL).read()) # Download the picture at the url as a file object
img = Image.open(f) # You can also use this on a local file; just put the local filename in quotes in place of f.
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so. 
width, height = img.size

#Process image and store (r, g, b) of each pixel in a list of tuples
def process(pix):              #returns [ (red_val <int>, green_val <int>, blue_val <int>) ]
    global width, height
    pixels = []
    for x in range(width):
        for y in range(height):
            r, g, b = pix[x, y]
            pixels.append((float(r), float(g), float(b), x, y))
    return pixels

#Choose k random, different pixels and store their vectors in a list called means
def strip(pixel):
    r, g, b, x, y = pixel
    return (r, g, b)

def find_means(k, pixels):           #returns means = [ vectors of k random pixels chosen from pixels ]
    means = []
    for i in range(k):
        randomind = random.randint(0, len(pixels)-1)
        if((pixel:=strip(pixels[randomind])) not in means): means.append(pixel)
    return means

#Loop through list of pixels and associate each pixel w/ a vector from means which is closest to its values (categorize them)
def calc_error(pixel, mean): 
    r, g, b, x, y = pixel
    r2, g2, b2 = mean
    return (r-r2)**2 + (g-g2)**2 + (b-b2)**2

def choosemean(pixel, means):
    min_mean, min_error = means[0], math.inf
    for mean in means:
        if((error:=calc_error(pixel, mean)) < min_error): min_error, min_mean = error, mean
    return min_mean

def addtodic(dic, mean, pixel):
    if(mean not in dic): dic.update({mean : [pixel]})
    else: dic[mean].append(pixel)

def categorize(means, pixels):         #returns { (vector_from_means) : [(pixel_vectors)] }
    meantopixels, pixelstomean = {}, {}
    for pixel in pixels:
        if(pixel not in pixelstomean):
            mean = choosemean(pixel, means)
            pixelstomean.update({pixel : mean})
        else: mean = pixelstomean[pixel]
        addtodic(meantopixels, mean, pixel)
    return meantopixels

#Loop through the dictionary of each mean and calculate the actual average vector of its associated pixels' data
def calc_average(pixels):            #returns average data vector for list of pixels
    n, totalr, totalg, totalb = len(pixels), 0, 0, 0
    for pixel in pixels:
        r, g, b, x, y = pixel
        totalr += r
        totalg += g
        totalb += b
    return (totalr/n, totalg/n, totalb/n)

def create_new_means(dic):
    new_means = []
    for mean in dic:
        pixels = dic[mean]
        new_means.append(calc_average(pixels))
    return new_means

def kmeans():
    count, x = 0, 0
    pixels = process(pix)
    means = find_means(K, pixels)
    prev_mean_pixels = {}

    while count <= 5:
        mean_pixels = categorize(means, pixels)
        if(prev_mean_pixels == mean_pixels): count += 1
        prev_mean_pixels = mean_pixels
        means = create_new_means(mean_pixels)
    return mean_pixels

def convert(mean_pixels):
    for mean in mean_pixels:
        meanr, meang, meanb = mean
        meanr, meang, meanb = int(round(meanr, 0)), int(round(meang, 0)), int(round(meanb, 0))
        for pixel in mean_pixels[mean]:
            pixr, pixg, pixb, x, y = pixel
            pix[x, y] = (meanr, meang, meanb)
    img.save("kmeansout.png")

convert(kmeans())

'''
#Part1: Naive Vector Quantization

def assignval(n, val):
    if(n == 27):
        if val < (255//3): return 0
        elif val > ((255*2)//3): return 255
        else: return 127
    elif(n == 8):
        if val < 128: return 0
        else: return 255

width, height = img.size

for x in range(width):
    for y in range(height):
        r, g, b = pix[x, y]
        pix[x, y] = (assignval(27, r), assignval(27, g), assignval(27, b))
img.show()
img.save("Naive_27.png")

for x in range(width):
    for y in range(height):
        r, g, b = pix[x, y]
        pix[x, y] = (assignval(8, r), assignval(8, g), assignval(8, b))
img.show()
img.save("Naive_8.png")
'''