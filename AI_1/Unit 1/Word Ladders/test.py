from os import pathsep
import sys
import time
from collections import deque

words = set()
indexes_to_check = []
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

with open("words_06_letters.txt") as f:
    for line in f:
        words.add(line.strip())

def find_indexes_to_check(start, goal):         #start and goal are lists
    inds_to_check = []
    for i in range(len(start)):
        if(start[i] != goal[i]): inds_to_check.append(i)
    return inds_to_check

def get_children(parent, itc):       #word and indexes_to_check are both lists
    children = []
    for index in itc:
        for letter in alphabet:
            temp = list(parent)
            temp[index] = letter
            if((st:=''.join(temp)) in words and st!=parent): children.append(st)
    return children

start = "foiled"
goal = "cooper"

indexes_to_check = find_indexes_to_check(start, goal)
print(indexes_to_check)
print(get_children(start, indexes_to_check))