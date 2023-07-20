import sys
import time
from collections import deque

'''
sample_board = "111..2|..3..2|003..2|6.3.44|6...5.|777.5."      "|" for clarity; actual string would only contain the dots and the letters, not the "|"
0s represent your board to get to goal
1 1 1 . . 2
. . 3 . . 2
0 0 3 . . 2 Goal
6 . 3 . 4 4
6 . . . 5 .
7 7 7 . 5 .
'''

#Global variables
board = "BCDDDEBC..FEGAA.FHGII.FH..J...KKJLL."
h_cars = {}                 #horizontal_cars = {num(str) : length(int)}
v_cars = {}                 #vertical_cars = {num(str) : length(int)}
path = []

def printboard(state):                      #state is a list
    for i in range(len(state)):
        if(i == 17): print(state[i] + " Goal" + "\n")
        elif(i == 35): print(state[i])
        elif((i+1) % 6 == 0): print(state[i] + "\n")
        else: print(state[i], end = " ")

def categorize_cars(state):
    visited = []
    for i in range(len(state)):
        if((num:=state[i]) != "." and num not in visited):
            visited.append(num)
            if(i<=33 and (num == state[i+1] == state[i+2])): h_cars.update({num : 3})
            elif(num == state[i+1]): h_cars.update({num : 2})
            elif((i <= 23) and num == state[i+6] == state[i+12]): v_cars.update({num : 3})
            elif(num == state[i+6]): v_cars.update({num : 2})

def dicadd(dic, car, ind):
    if(car not in dic): dic.update({car : [ind]})
    else: dic[car].append(ind)

def current_indexes(state):
    temp, dic = list(state), {}
    for i in range(len(temp)):
        if(temp[i] != "."): dicadd(dic, temp[i], i)
    return dic

def get_children(parent):               #parent is string and indexOf always return first index
    indexesdic = current_indexes(parent)             #indexsdic = { carnum : [indexes] }
    car_Lindexes, car_Rindexes = get_possible_hindexes(parent, indexesdic)
    car_Tindexes, car_Bindexes = get_possible_vindexes(parent, indexesdic)
    return generateLstates(parent, car_Lindexes, indexesdic) + generateRstates(parent, car_Rindexes, indexesdic) + generateTstates(parent, car_Tindexes, indexesdic) + generateBstates(parent, car_Bindexes, indexesdic)

def clearboard(state, car, indexesdic):
    for i in indexesdic[car]:
        state[i] = "."

def generateLstates(parent, car_Lindexes, indexesdic):
    lstates = []
    for car in car_Lindexes:
        length = h_cars[car]
        for index in car_Lindexes[car]:
            state = list(parent)
            clearboard(state, car, indexesdic)                      #erase car from board
            for i in range(index, index+length):               #fillboard with car
                state[i] = car
            lstates.append(''.join(state))
    return lstates

def generateRstates(parent, car_Rindexes, indexesdic):
    rstates = []
    for car in car_Rindexes:
        length = h_cars[car]
        for index in car_Rindexes[car]:
            state = list(parent)
            clearboard(state, car, indexesdic)                      #erase car from board
            for i in range(index-length+1, index+1):               #fillboard with car
                state[i] = car
            rstates.append(''.join(state))
    return rstates

def generateTstates(parent, car_Tindexes, indexesdic):
    tstates = []
    for car in car_Tindexes:
        length = v_cars[car]
        for index in car_Tindexes[car]:
            state = list(parent)
            clearboard(state, car, indexesdic)                      #erase car from board
            for i in range(index, index+((length-1)*6)+1, 6):               #fillboard with car
                state[i] = car
            tstates.append(''.join(state))
    return tstates
    
def generateBstates(parent, car_Bindexes, indexesdic):
    bstates = []
    for car in car_Bindexes:
        length = v_cars[car]
        for index in car_Bindexes[car]:
            state = list(parent)
            clearboard(state, car, indexesdic)                      #erase car from board
            for i in range(index-((length-1)*6), index+1, 6):               #fillboard with car
                state[i] = car
            bstates.append(''.join(state))
    return bstates

def get_possible_hindexes(parent, dic):                                                #parent is string
    car_leftpossibleindex, car_rightpossibleindex = {}, {}                        #{carnum(str) : [possibleindex(int)]}
    for car in h_cars.keys():
        state = list(parent)
        leftindex, length = dic[car][0], h_cars[car]
        rightindex = leftindex + length - 1
        while((leftindex%6!=0) and (state[leftindex-1] == ".")):                  #Checking indexes to the left of car
            dicadd(car_leftpossibleindex, car, leftindex-1)
            leftindex -= 1
        while(((rightindex+1)%6!=0) and (state[rightindex+1] == ".")):            #Checking indexes to the right of car
            dicadd(car_rightpossibleindex, car, rightindex+1)
            rightindex += 1
    return (car_leftpossibleindex, car_rightpossibleindex)

def get_possible_vindexes(parent, dic):                                                #parent is string
    car_toppossibleindex, car_bottompossibleindex = {}, {}                        #{carnum(str) : [possibleindex(int)]}
    for car in v_cars.keys():
        state = list(parent)
        topindex, length = dic[car][0], v_cars[car]
        bottomindex = ((length-1) * 6) + topindex
        while((topindex>5) and (state[topindex-6] == ".")):                       #Checking indexes above car
            dicadd(car_toppossibleindex, car, topindex-6)
            topindex -= 6
        while((bottomindex<30) and (state[bottomindex+6] == ".")):                #Checking indexes below car
            dicadd(car_bottompossibleindex, car, bottomindex+6)
            bottomindex += 6
    return (car_toppossibleindex, car_bottompossibleindex)

def goal_test(state):
    return "A" == state[16] == state[17]

def process(start, goal, c_p):
    count = 0
    path.append(goal)
    while(goal in c_p and goal != start):
        goal = c_p[goal]
        path.append(goal)
        count+=1
    return count

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

categorize_cars(board)
print("Minimum number of moves requires to solve board: %s" % BFS(board))
print("Path:")
for i in range(len(path)-1, -1, -1): 
    print(path[i])
    print("--------------------------")