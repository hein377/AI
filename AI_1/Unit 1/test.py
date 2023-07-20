from os import pathsep
import sys
import time
from collections import deque

words = set()
indexes_to_check = []
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

with open("%s" % sys.argv[1]) as f:
    line_list = [line.strip() for line in f]

def find_indexes_to_check(start, goal):         #start and goal are lists
    inds_to_check = []
    for i in range(len(start)):
        if(start[i] != goal[i]): inds_to_check.append(i)
    return inds_to_check

def get_children(parent):       #word and indexes_to_check are both lists
    children = []
    for index in indexes_to_check:
        for letter in alphabet:
            print("index: %s   letter: %s" % (index, letter))
            temp = parent
            temp[index] = letter
            if((st:=''.join(temp)) in words): children.append(st)
            print(temp)
            print(children)
            print(''.join(temp))
            input()
    return children

indexes_to_check = find_indexes_to_check("abased", "abases")
print(indexes_to_check)
print(words)
print(get_children(list("abased")))