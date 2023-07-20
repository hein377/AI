from os import pathsep
import sys
import time
from collections import deque

with open("%s" % sys.argv[1]) as f:
    line_list = [line.strip() for line in f]

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

def BFS(start):
    fringe, visited, child_parent = deque(), {start}, {start:''}
    fringe.append(start)
    while(len(fringe) != 0):
        v = fringe.popleft()
        if(goal_test(v)):
            return process(start, v, child_parent)        #len of min path
        for c in get_children(v):
            if(c not in visited):
                if(v in child_parent): child_parent.update({c:v})
                fringe.append(c)
                visited.add(c)
    return None

def startbiprocess(start, end, c, v, c_p):
    count = 1       #unaccounted move from c to v
    while(v in c_p and v != start): v, count = c_p[v], count+1
    while(c in c_p and c != end): c, count = c_p[c], count+1
    return count

def endbiprocess(start, end, c, v, c_p):
    count = 1       #unaccounted move from c to v
    while(v in c_p and v != end): v, count = c_p[v], count+1
    while(c in c_p and c != start): c, count = c_p[c], count+1
    return count

def bi_BFS(start):
    fringe, visited, endfringe, endvisited, child_parent = deque(), {start}, deque(), {(end:=find_goal(start))}, {start:'', end:''}
    fringe.append(start)
    endfringe.append(end)
    while(len(fringe) != 0 or len(endfringe != 0)):
        v = fringe.popleft()
        for c in get_children(v):
            if(c not in visited):
                if(c in child_parent):
                    return startbiprocess(start, end, c, v, child_parent)
                if(v in child_parent): child_parent.update({c:v})
                fringe.append(c)
                visited.add(c)
        v = endfringe.popleft()
        for c in get_children(v):
            if(c not in endvisited):
                if(c in child_parent):
                    return endbiprocess(start, end, c, v, child_parent)
                if(v in child_parent): child_parent.update({c:v})
                endfringe.append(c)
                endvisited.add(c)
    return None
    
def hardest_Puzzle(goal):
    fringe, visited, ls, child_parent, longestboard_lenpath_path = deque(), {goal}, [], {goal:''}, []
    fringe.append(goal)
    while(len(fringe) != 0):
        v = fringe.popleft()
        ls.append(v)
        for c in get_children(v):
            if(c not in visited):
                if(v in child_parent): child_parent.update({c:v})
                fringe.append(c)
                visited.add(c)
    x = process(goal, ls[-1], child_parent)
    for i in range(len(ls)-1, 0, -1):
        len_path, path = process2(goal, ls[i], child_parent)
        if(len_path == x):
            longestboard_lenpath_path.append((ls[i],len_path, path))
    return longestboard_lenpath_path

def process(start, goal, c_p):
    count = 0
    while(goal in c_p and goal != start):
        goal = c_p[goal]
        count+=1
    return count

def process2(start, goal, c_p):
    count = 0
    ls = [goal]
    while(goal in c_p and goal != start):
        goal = c_p[goal]
        ls.append(goal)
        count+=1
    return count, ls

for i in range(len(line_list)):
    x = line_list[i].split()
    start = time.perf_counter()
    print("BFS: Line %s: %s, %s moves found in " % (i, x[1], BFS(x[1])), end = '')
    end = time.perf_counter()
    print(end - start)

    start = time.perf_counter()
    print("BiBFS: Line %s: %s, %s moves found in " % (i, x[1], bi_BFS(x[1])), end = '')
    end = time.perf_counter()
    print(end - start)
'''''
function BFS(start-node):
fringe = new Queue()
visited = new Set()
fringe.add(start-node)
visited.add(start-node)
while fringe is not empty do:
v = fringe.pop()
if GoalTest(v) then:
return v
for every child c of v do:
if c not in visited then:
fringe.add(c)
visited.add(c)
return None
'''''