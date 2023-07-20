from os import pathsep
import sys
import time
from collections import deque
from heapq import heappush, heappop, heapify

with open("%s" % sys.argv[1]) as f:
    line_list = [line.strip() for line in f]

def parity_check(board, size):
    x = countoutoforder(board)
    if(size == 2): return x!=0
    elif(size == 3 or size == 5): return x%2==0
    elif(size == 4): return (x%2!=0 and inevenrow(board, size)) or (x%2==0 and not inevenrow(board, size))
    return False

def countoutoforder(board):
    ls, count = list(board), 0
    for i in range(1, len(board)):
        for x in range(i-1, -1, -1):
            if(board[i] != '.' and board[x] != '.' and (board[i] < board[x])): count+=1
    return count

def inevenrow(board, size):
    ind = board.index('.')
    return (ind//size) % 2 != 1

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

def process(start, goal, c_p):
    count = 0
    while(goal in c_p and goal != start):
        goal = c_p[goal]
        count+=1
    return count

def k_DFS(start_state, k):
    fringe, start_node = deque(), (start_state, 0, {start_state})
    fringe.append(start_node)
    while(len(fringe) != 0):
        state, depth, ancestors = fringe.pop()
        if(goal_test(state)): return depth
        if(depth < k):
            for c in get_children(state):
                if(c not in ancestors):
                    ancestors2 = ancestors.copy()
                    ancestors2.add(c)
                    fringe.append((c, depth+1, ancestors2))
    return None

def ID_DFS(start_state):
    max_depth = 0
    result = None
    while(result is None):
        result = k_DFS(start_state, max_depth)
        max_depth += 1
    return result

def taxi_cab(board, size):
    moves = 0
    goal = find_goal(board)
    for ind in range(len(board)):
        if(board[ind] != "."):
            element = board[ind]
            goalind = goal.index(element)
            element_row, goal_row = ind//size, goalind//size
            element_col, goal_col = ind%size, goalind%size
            moves += (abs(goal_row - element_row) + abs(element_col - goal_col))
    return moves

def a_star(start_state):
    fringe, closed, start_node = [], set(), (taxi_cab(start_state, size), start_state, 0)            #start_node = (f(x), state, depth)
    heappush(fringe, start_node)
    while(len(fringe) != 0):
        node = heappop(fringe)
        f, state, depth = node
        if goal_test(state): return f
        if state not in closed:
            closed.add(state)
            for c in get_children(state):
                if c not in closed:
                    temp = (depth+1+taxi_cab(c, size), c, depth+1)
                    heappush(fringe, temp)
    return None

for i in range(len(line_list)):
    x=line_list[i]
    size = int(x[0])
    board = x[2:2+(size**2)]
    norman = x[-1]
    start = time.perf_counter()
    parity = parity_check(board, size)
    end = time.perf_counter()
    if(not parity): 
        print("Line %s: %s, no solution determined in " % (i, board), end = '')
        print(str(end - start) + " seconds \n")
    else:
        if(norman == '!'):
            start = time.perf_counter()
            print("Line %s: %s, BFS - %s moves found in " % (i, board, BFS(board)), end = '')
            end = time.perf_counter()
            print(str(end - start) + " seconds")

            start = time.perf_counter()
            print("Line %s: %s, IDDFS - %s moves found in " % (i, board, ID_DFS(board)), end = '')
            end = time.perf_counter()
            print(str(end - start) + " seconds")

            start = time.perf_counter()
            print("Line %s: %s, A* - %s moves found in " % (i, board, a_star(board)), end = '')
            end = time.perf_counter()
            print(str(end - start) + " seconds \n")

        elif(norman == 'B'):
            start = time.perf_counter()
            print("Line %s: %s, BFS - %s moves found in " % (i, board, BFS(board)), end = '')
            end = time.perf_counter()
            print(str(end - start) + " seconds \n")

        elif(norman == 'I'):
            start = time.perf_counter()
            print("Line %s: %s, IDDFS - %s moves found in " % (i, board, ID_DFS(board)), end = '')
            end = time.perf_counter()
            print(str(end - start) + " seconds \n")

        elif(norman == 'A'):
            start = time.perf_counter()
            print("Line %s: %s, AStar - %s moves found in " % (i, board, a_star(board)), end = '')
            end = time.perf_counter()
            print(str(end - start) + " seconds \n")

'''
function k-DFS(start-state, k):
    fringe = new Stack()
    start_node = new Node()
    start_node.state = start-state
    start_node.depth = 0
    start_node.ancestors = new Set()
    start_node.ancestors.add(start-state)
    fringe.add(start-node)
    while fringe is not empty do:
        v = fringe.pop()
        if GoalTest(v) then:
            return v
        if v.depth < k:
            for every child c of v do:
                if c not in v.ancestors then:
                    temp = new Node()
                    temp.state = c
                    temp.depth = v.depth + 1
                    temp.ancestors = v.ancestors.copy()
                    temp.ancestors.add(c)
                    fringe.add(temp)
    return None

function ID-DFS(start-state):
    max_depth = 0
    result = None
    while result is None:
        result = k-DFS(start-state, max_depth)
        max_depth = max_depth + 1
    return result

function a_star(start-state):
    closed = new Set()
    start_node = new Node()
    start_node.state = start-state
    start_node.depth = 0
    start_node.f = heuristic(start-state)
    fringe = new Heap()
    fringe.add(start_node)
    while fringe is not empty do:
        v = fringe.pop()
        if GoalTest(v):
            return(v)
        if v.state not in closed:
            closed.add(v.state)
            for each child c of v do:
                if c not in closed:
                    temp = new Node()
                    temp.state = c
                    temp.depth = v.depth + 1
                    temp.f = temp.depth + heuristic(c)
                    fringe.add(temp)
    return None
'''