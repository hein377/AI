from os import pathsep
import sys
import time
import random

#Global Variables
n = 0
sb_height = 0
sb_width = 0
symbol_set = []
symbol_dict = {}            #{symbol : #of_occurrences}
constraint_set = []
neighbors = {}              #{index : set(neighbors)}

def printboard(board):          #board is a string
    global n, sb_width, sb_height
    for i in range(len(board)):
        if((i+1)%(n*sb_height) == 0):
            print(board[i])
            for i in range((sb_width*4)): print("--", end = "")
            print()
        elif((i+1)%n == 0): print(board[i])
        elif((i+1)%sb_width == 0): print(board[i], end = " | ")
        else: print(board[i], end = " ")

#Dimensions (height and width setup)
def find_factors():
    global n
    factors = []
    for i in range(2, int(n**0.5)+1):
        if(n%i == 0): factors += [i, n//i]
    factors.sort()
    return factors

def get_Dimensions():                                               #returns (width, height)
    global n
    root, factors = n**0.5, {}
    if((x:=int(root)) * x == n): return x, x
    else:
        factors = find_factors()
        for i in range(len(factors)):
            if factors[i] > root:
                return (factors[i], factors[i-1])

#Symbols
def find_symbolset():
    global n
    alphabet, ls = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"], []
    for i in range(1,n+1):
        if(i > 9): ls.append(alphabet[i-10])
        else: ls.append(str(i))
    return ls

def addtodic(dic, symbol):
    if(symbol not in dic): dic.update({symbol:1})
    else: dic[symbol]+=1

def find_symbolsFrequency(board):
    dic = {}
    for symbol in board:
        if(symbol != "."): addtodic(dic, symbol)
    return dic

#Constraintset
def find_constraintset():
    global n, sb_width, sb_height
    return row_constraintsets(n) + col_constraintsets(n) + block_constraintsets(sb_width, sb_height)

def row_constraintsets(n):
    rowlist = []
    for i in range(0, n*n, n):
        s = set()
        for x in range(i, i+n): s.add(x)
        rowlist.append(s)
    return rowlist

def col_constraintsets(n):
    collist = []
    for i in range(n):
        s = set()
        for x in range(i, (n*(n-1))+i+1, n): s.add(x)
        collist.append(s)
    return collist

def block_constraintsets(width, height):
    blocklist = []
    for h in range(height):
        for ind in range(y:=(h*width), ((n//height-1) * (x:=(height*height*width))) + 1 + y, x):
            s = set()
            for i in range(ind, ind + 1 + ((height-1)*n), n):
                for col in range(i, i+width):
                    s.add(col)
            blocklist.append(s)
    return blocklist

#Neighbors
def dicadd(dic, key, val):
    val.remove(key)
    if(key not in dic): dic.update({key : val})
    else: dic[key].update(val)

def find_neighbors():
    global n, constraint_set
    dic = {}
    for ind in range(n*n):
        for sets in constraint_set:
            temp = sets.copy()
            if(ind in sets): dicadd(dic, ind, temp)
    return dic

#BackTrack
#GoalTest
def goal_test(state):
    global sb_width, sb_height
    if("." in state): return False
    return rowtest(state) and coltest(state) and blocktest(state, sb_width, sb_height)

def rowtest(state):
    for row in range(0, (n*(n-1))+1, n):
        s = set(state[row])
        for col in range(row+1, row+n): s.add(state[col])
        if(len(s) != n): return False
    return True

def coltest(state):
    for col in range(0, n):
        s = set(state[col])
        for row in range(col+n, (n*(n-1)) + col + 1, n): s.add(state[row])
        if(len(s) != n): return False
    return True

def blocktest(state, width, height):
    area = width * height
    for h in range(height):
        for ind in range(y:=(h*width), ((n//height-1) * (x:=(height*height*width))) + 1 + y, x):
            s = set()
            for i in range(ind, ind + 1 + ((height-1)*n), n):
                for col in range(i, i+width): s.add(state[col])
            if(len(s) != area): return False
    return True
    
def get_next_unassigned_var(state):     #first "."
    return state.index(".")

def neighborcheck(state, ind, symbol):
    global neighbors
    for neighborind in neighbors[ind]:
        if(state[neighborind] == symbol): return False
    return True

def get_sorted_values(state, ind):      #possible symbols to try
    global symbol_set, neighbors
    pos_symbols = []
    for symbol in symbol_set:
        if(neighborcheck(state, ind, symbol)): pos_symbols.append(symbol)
    return pos_symbols

def csp_backtracking(state):        #state is a list
    if goal_test(state): return state
    ind = get_next_unassigned_var(state)
    sorted_values = get_sorted_values(state, ind)
    for i in range(length:=len(sorted_values)):
        symbol = sorted_values[i]
        new_state = list(state)            #create new_state by assigning val to var
        new_state[ind] = symbol
        result = csp_backtracking(''.join(new_state))
        if result is not None: return result
    return None

with open("%s" % sys.argv[1]) as f:
    for line in f:
        board = line.strip()
        n = int(len(board)**(0.5))
        print("board: %s   n: %s" % (board, n))
        sb_width, sb_height = get_Dimensions()
        symbol_set = find_symbolset()
        constraint_set = find_constraintset()
        neighbors = find_neighbors()
        symbol_dict = find_symbolsFrequency
        print(csp_backtracking(board))