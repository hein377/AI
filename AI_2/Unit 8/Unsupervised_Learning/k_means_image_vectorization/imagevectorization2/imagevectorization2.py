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

#Process image and store (r, g, b) of each pixel in a list of tuples
def process(pix):              #returns { (red_val <int>, green_val <int>, blue_val <int>) : [(x,y), ...]<list of tuples of intsj> }
    pix_loc = {}
    for x in range(WIDTH):
        for y in range(HEIGHT):
            r, g, b = pix[x, y]
            r, g, b = float(r), float(g), float(b)
            if((r,g,b) not in pix_loc): pix_loc.update({(r,g,b) : [(x,y)]})
            else: pix_loc[(r,g,b)].append((x,y))
    return pix_loc

PIX_LOC = process(pix)

#Chossing initial centroids
#Implement k-means++ algorithm
def find_distance(pixels, centroids):       #returns distance of each pixel to nearest centroid; pixels = [ (r,g,b), ... ]
    pixel_distance = {}
    for pixel in pixels:
        distances = []
        r, g, b = pixel
        for centroid in centroids:
            r2, g2, b2 = centroid
            distances.append(math.sqrt((r-r2)**2 + (g-g2)**2 + (b-b2)**2))
        pixel_distance.update({pixel:min(distances)})
    return pixel_distance,sorted(list(pixel_distance.keys()), key = lambda x: pixel_distance[x], reverse = True)

def choose_centroid(pixel_distance, sorted_pixels):         #sorted_pixels = [ pixels_with_furthest_distance --> pixels_with_closest_distance ]
    for pixel in sorted_pixels:
        if((d:=pixel_distance[pixel]) != 0):
            prob = 2*(1/d)
            if(random.uniform(0,1) > prob): return pixel
    return None

def find_initial_means(k, pixels):           #returns means = [ vectors of k centroid pixels ]
    centroids = [pixels[random.randint(0,len(pixels)-1)]]
    while (len(centroids) != k):
        pixel_distance, sorted_pixels = find_distance(pixels, centroids)
        centroids.append(choose_centroid(pixel_distance, sorted_pixels))
    return centroids

#Choose random k centroids
def find_means(k, pixels):           #returns means = [ vectors of k random pixels chosen from pixels ]
    means, random_inds = [], sample(range(0,len(pixels)),k)
    return [pixels[i] for i in random_inds]

#Loop through list of pixels and associate each pixel w/ a vector from means which is closest to its values (categorize them)
def calc_error(pixel, mean): 
    r, g, b = pixel
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
    meantopixels = {}
    for pixel in pixels:
        mean = choosemean(pixel, means)
        addtodic(meantopixels, mean, pixel)
    return meantopixels

#Loop through the dictionary of each mean and calculate the actual average vector of its associated pixels' data
def calc_average(pixels):            #returns average data vector for list of pixels
    global PIX_LOC
    total_numpixels, totalr, totalg, totalb = 0, 0, 0, 0
    for pixel in pixels:
        num_pixels = len(PIX_LOC[pixel])
        total_numpixels += num_pixels
        r, g, b = pixel
        totalr += (r*num_pixels)
        totalg += (g*num_pixels)
        totalb += (b*num_pixels)
    return (totalr/total_numpixels, totalg/total_numpixels, totalb/total_numpixels)

def create_new_means(dic):
    new_means = []
    for mean in dic:
        pixels = dic[mean]
        new_means.append(calc_average(pixels))
    return new_means

def kmeans():
    global PIX_LOC
    prev_mean_pixels, count, generation = {}, 0, 1
    pixels = list(PIX_LOC.keys())
    means = find_initial_means(K, pixels)
    #means = find_means(K, pixels)

    while count <= 5:
        mean_pixels = categorize(means, pixels)
        if(prev_mean_pixels == mean_pixels): count += 1
        prev_mean_pixels = mean_pixels
        means = create_new_means(mean_pixels)
        generation += 1
    return mean_pixels, generation

#Colorbands
def create_colorband_image(mean_pixels):
    colorbox_height = colorbox_width = math.floor(WIDTH / K)
    cb_img_width, cb_img_height = WIDTH, HEIGHT + colorbox_height
    cb_img = Image.new("RGB", (cb_img_width, cb_img_height), 0)
    cb_pix = cb_img.load()
    x = 0
    for mean in mean_pixels:
        r, g, b = mean
        for row in range(x, x+colorbox_width):
            for col in range(HEIGHT, cb_img_height):
                cb_pix[row, col] = (r, g, b)
        x = x+colorbox_width
    cb_img.paste(img, (0,0))
    return cb_img

def round_mean(mean_pixels):
    dic = {}
    for mean in mean_pixels:
        r, g, b = mean
        rounded_mean = (int(round(r, 0)), int(round(g, 0)), int(round(b, 0)))
        dic.update({rounded_mean:mean_pixels[mean]})
    return dic

#Dithering
'''for each y from top to bottom do
    for each x from left to right do
        oldpixel := pixels[x][y]
        newpixel := find_closest_palette_color(oldpixel)
        pixels[x][y] := newpixel
        quant_error := oldpixel - newpixel
        pixels[x + 1][y    ] := pixels[x + 1][y    ] + quant_error × 7 / 16
        pixels[x - 1][y + 1] := pixels[x - 1][y + 1] + quant_error × 3 / 16
        pixels[x    ][y + 1] := pixels[x    ][y + 1] + quant_error × 5 / 16
        pixels[x + 1][y + 1] := pixels[x + 1][y + 1] + quant_error × 1 / 16
'''
def tup_add(tup1, tup2): 
    return tuple([int(round(tup1[i],0)) + int(round(tup2[i],0)) for i in range(len(tup1))])

def tup_mult(tup1, scalar):
    return tuple([e * scalar for e in tup1])

def dither(coord_mean):                               #already rounded means
    for x in range(WIDTH):
        for y in range(HEIGHT):
            r, g, b = pix[x,y]
            r2, g2, b2 = coord_mean[(x,y)]
            pix[x,y] = (int(round(r2, 0)), int(round(g2, 0)), int(round(b2, 0)))
            quant_error = (r-r2,g-g2,b-b2)

            if(x!=(WIDTH-1)): pix[x+1,y] = tup_add(pix[x+1,y], tup_mult(quant_error, 7 / 16))
            if(x!=0 and y!=(HEIGHT-1)): pix[x-1,y+1] = tup_add(pix[x-1,y+1], tup_mult(quant_error, 3 / 16))
            if(y!=(HEIGHT-1)): pix[x,y+1] = tup_add(pix[x,y+1], tup_mult(quant_error, 5 / 16))
            if(x!=(WIDTH-1) and y!=(HEIGHT-1)): pix[x+1,y+1] = tup_add(pix[x+1,y+1], tup_mult(quant_error, 1 / 16))

def find_coordmean(mean_pixels):
    global PIX_LOC
    coord_mean = {}
    for mean in mean_pixels:
        for pixel in mean_pixels[mean]: 
            for coords in PIX_LOC[pixel]:
                for coord in coords: coord_mean.update({coord:mean})
    return coord_mean

def convert(mean_pixels):
    global PIX_LOC
    rounded_mp, coord_mean = round_mean(mean_pixels), find_coordmean(mean_pixels)

    dither(coord_mean)
    pickle.dump(rounded_mp, open('mean_pixels.pkl', 'wb'))
    means = list(rounded_mp.keys())
    f = open("k-means_means.txt", "w")
    f.write(str(means))
    f.close()
    final_img = create_colorband_image(rounded_mp)
    final_img.show()
    final_img.save("k-means_output.png")

print("KMEANS++")
#print("RANDOM_MEANS")

t, g = 0, 0
for i in range(10):
    start = time.perf_counter()
    mean_pixels, generation = kmeans()
    convert(mean_pixels)
    end = time.perf_counter()
    t += end - start
    g += generation
    print(f"Iteration {i} Time Taken: {end-start}       Num_Generations: {generation}")
print(f"Average Time Taken: {t/10}")
print(f"Average Generation Taken: {g/10}")

'''img = Image.open("puppy_8_means.png")
img.show()
input()
savefile = open('mean_pixels.pkl', 'rb')
mean_pixels = pickle.load(savefile)
final_img = create_colorband_image(mean_pixels)
final_img.show()
input()
final_img.save("kmeansout.png")'''