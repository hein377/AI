from os import pathsep
import sys
import time
from collections import deque

def print_puzzle(size, str):
    ls = list(str)
    for i in range(int(size**2)):
        print("%s " % ls[i],end='')
        if((i+1)%size == 0):
            print()

def find_goal(str):
    start = list(str)
    goal = ''.join(sorted(start))
    return goal[1:] + goal[0]

def get_children(str):
    size = int(len(str)**0.5)
    si, lis= int(size**2), list(str)
    pos, ls, lb, rb = lis.index('.'), [], {x for x in range(0,si, size)}, {x for x in range(size-1, si, size)}
    if(pos-size >= 0): ls.append(swap(lis, pos, pos-size))
    if(pos+size < si): ls.append(swap(lis, pos, pos+size))
    if(pos not in lb): ls.append(swap(lis, pos, pos-1))
    if(pos not in rb): ls.append(swap(lis, pos, pos+1))
    return ls

def swap(lis, x, y):
    ls = lis.copy()
    temp = ls[x]
    ls[x] = ls[y]
    ls[y] = temp
    return ''.join(ls)

def goal_test(str):
    return str == find_goal(str)

def BFS(start):         #start = goal
    fringe, visited, child_parent = deque(), {start}, {start:''}
    fringe.append(start)
    while(len(fringe) != 0):
        v = fringe.popleft()
        for c in get_children(v):
            if(c not in visited):
                if(v in child_parent): child_parent.update({c:v})
                fringe.append(c)
                visited.add(c)
    return len(visited)

print(BFS('ABCDEFGH.'))