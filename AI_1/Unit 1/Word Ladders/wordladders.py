import sys
import time
from collections import deque

#Global Variables
start = ""
goal = ""
words = set()
path = []               #Path is backwards; [goal --> start]
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
total_time = 0
children = {}           #{ parent : [children] }
nochildren = []

def goal_test(str):
    return str == goal

def process(start, goal, c_p):
    count = 1
    path.append(goal)
    while(goal in c_p and goal != start):
        goal = c_p[goal]
        path.append(goal)
        count+=1
    return count

def get_children(parent):
    childs = []
    for i in range(len(parent)):
        for letter in alphabet:
            temp = list(parent)
            temp[i] = letter
            if((st:=''.join(temp)) in words and st!=parent): childs.append(st)
    return childs

def BFS(start):
    global children
    fringe, visited, child_parent = deque(), {start}, {start:''}
    fringe.append(start)
    while(len(fringe) != 0):
        v = fringe.popleft()
        if(goal_test(v)):
            return process(start, v, child_parent)        #len of min path
        for c in children[v]:
            if(c not in visited):
                if(v in child_parent): child_parent.update({c:v})
                fringe.append(c)
                visited.add(c)
    return None

with open("%s" % sys.argv[1]) as f:                         #Establishing words set
    for line in f: words.add(line.strip())

with open("%s" % sys.argv[1]) as f:                         #Establishing children dictionary
    for line in f: children.update({(word:=line.strip()) : get_children(word)})

with open("%s" % sys.argv[2]) as f:
    count = 0
    for line in f:
        line_list, path = line.strip().split(' '), []         #line_list = [start, goal]
        start, goal = line_list[0], line_list[1]
        print("Line: %s" % count)
        begin = time.perf_counter()
        length = BFS(start)
        end = time.perf_counter()
        total_time += (end - begin)
        if(length == 0): print("No solution!\n")
        else:
            print("Length is: %s" % length)
            for i in range(len(path)-1, -1, -1):
                print(path[i])
        print()
        count+=1
print("Time to solve all of these puzzles was: %s seconds" % total_time)