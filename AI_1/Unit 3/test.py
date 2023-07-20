from os import pathsep
import sys

#Global Varaibles
minlen = 0
dic = []            #list of valid words
game = ""

with open("%s" % sys.argv[1]) as f:
    for line in f:
        if line.strip().isalpha(): dic.append(line.strip().lower())

print(dic)