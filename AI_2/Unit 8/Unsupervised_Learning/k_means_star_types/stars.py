import random
import math
from venv import create

#Process star_data and store it in a list of tuples
def process(filename):              #returns [ (Temperature <int>, Luminosity <float>, Radius <float>, Absolute magnitude <float>, Star type <int>) ]
    stars = []
    with open(filename) as f:
        for line in f:
            if("Temperature (K)" not in line.strip().split(",")):
                ls = line.strip().split(",")
                stars.append((math.log(float(ls[0])), math.log(float(ls[1])), math.log(float(ls[2])), float(ls[3]), int(ls[4])))
    return stars

#Choose k = 6 random, different stars and store their vectors in a list called means
def strip(star):
    temp, lum, rad, mag, star_type = star
    return (temp, lum, rad, mag)

def find_means(k, starsls):           #returns means = [ vectors of k random stars chosen from starsls ]
    means = []
    for i in range(k):
        randomind = random.randint(0, len(starsls)-1)
        if((star:=strip(starsls[randomind])) not in means): means.append(star)
    return means

#Loop through list of stars and associate each star w/ a vector from means which is closest to its values (categorize them)
def calc_error(star, mean): 
    temp, lum, rad, mag, star_type = star
    temp2, lum2, rad2, mag2 = mean
    return (temp-temp2)**2 + (lum-lum2)**2 + (rad-rad2)**2 + (mag-mag2)**2

def choosemean(star, means):
    min_mean, min_error = means[0], math.inf
    for mean in means:
        if((error:=calc_error(star, mean)) < min_error): min_error, min_mean = error, mean
    return min_mean

def addtodic(dic, mean, star):
    if(mean not in dic): dic.update({mean : [star]})
    else: dic[mean].append(star)

def categorize(means, stars):         #returns { (vector_from_means) : [(star_vectors)] }
    dic = {}
    for star in stars:
        mean = choosemean(star, means)
        addtodic(dic, mean, star)
    return dic

#Loop through the dictionary of each mean and calculate the actual average vector of its associated stars' data
def calc_average(stars):            #returns average data vector for list of stars
    n, totaltemp, totallum, totalradius, totalmagnitutde = len(stars), 0, 0, 0, 0
    for star in stars:
        temp, lum, rad, mag, star_type = star
        totaltemp += temp
        totallum += lum
        totalradius += rad
        totalmagnitutde += mag
    return (totaltemp/n, totallum/n, totalradius/n, totalmagnitutde/n)

def create_new_means(dic):
    new_means = []
    for mean in dic:
        stars = dic[mean]
        new_means.append(calc_average(stars))
    return new_means

count = 0
stars = process("star_data.csv")
means = find_means(6, stars)
prev_mean_stars = {}

while count <= 5:
    mean_stars = categorize(means, stars)
    if(prev_mean_stars == mean_stars): count += 1
    prev_mean_stars = mean_stars
    means = create_new_means(mean_stars)

for mean in mean_stars:
    print(f"MEAN: {mean}")
    print(f"star_type: ")
    for star in mean_stars[mean]:
        temp, lum, rad, mag, star_type = star
        print(f"{star_type}", end = " ")
    print("\n")
'''
 Brown Dwarf -> Star Type = 0
 Red Dwarf -> Star Type = 1
 White Dwarf-> Star Type = 2
 Main Sequence -> Star Type = 3
 Supergiant -> Star Type = 4
 Hypergiant -> Star Type = 5
'''