#Global Variables
board = ""                  #{index : str_of_possibilities}
n = 0
sb_height = 0
sb_width = 0
symbol_set = []
symbol_dict = {}            #{symbol : #of_occurrences}
constraint_set = []
neighbors = {}              #{index : set(neighbors)}
solved_inds = set()             #for forward looking

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

def makeboard(b):
    dic = {}
    for i in range(len(b)):
        if((item:=b[i]) == "."): dic.update({i : ''.join(symbol_set)})
        elif(item in symbol_set):
            solved_inds.add(i)
            dic.update({i : item})
    return dic

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
    for ind, symbol in board.items():
        if(len(symbol) != 1): addtodic(dic, symbol)
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


#Forward_Looking
def forward_looking(board, solvedinds):
    while(len(solvedinds) != 0):
        ind = solvedinds.pop()
        for i in neighbors[ind]:
            if(i not in solvedinds and (solveditem:=board[ind]) in (curitem:=board[i])):
                temp = list(curitem)
                temp.remove(solveditem)
                board[i] = ''.join(temp)
                if(len(temp) == 1): solvedinds.add(i)
    return constraint_propagation(board)

#Constraint_Propagation
def dicadd2(dic, symbol, ind):
    if(symbol not in dic): dic.update({symbol : [ind]})
    else: dic[symbol].append(ind)

def process_set(s):
    symbol_ind, val_ind = {}, []
    for i in s:
        for symbol in list(board[i]):
            dicadd2(symbol_ind, symbol, i)
    for symbol, indlist in symbol_ind.items():
        if(len(indlist) == 1): val_ind.append((symbol, indlist[0]))
    return val_ind

def constraint_propagation(board):
    global constraint_set
    newly_solvedinds = set()
    for s in constraint_set:                #s is a set
        for (val, ind) in process_set(s):
            if(len(board[ind]) != 1):
                newly_solvedinds.add(ind)
                board[ind] = val
    if(len(newly_solvedinds) != 0): forward_looking(board, newly_solvedinds)
    return board

def assign(board, var, val):
    board[var] = str(val)

board = {0: '5', 1: '3', 2: '2', 3: '4', 4: '168', 5: '168', 6: '68', 7: '9', 8: '7', 9: '47', 10: '9', 11: '1', 12: '368', 13: '2', 14: '35678', 15: '4568', 16: '456', 17: '34568', 18: '47', 19: '6', 20: '8', 21: '9', 22: '157', 23: '1357', 24: '2', 25: '145', 26: '1345', 27: '3', 28: '7', 29: '6', 30: '5', 31: '4', 32: '9', 33: '1', 34: '8', 35: '2', 36: '2', 37: '1458', 38: '45', 39: '168', 40: '1678', 41: '1678', 42: '3', 43: '4567', 44: '9', 45: '9', 46: '1458', 47: '45', 48: '2', 49: '3', 50: '1678', 51: '456', 52: '4567', 53: '456', 54: '6', 55: '45', 56: '3', 57: '7', 58: '9', 59: '2', 60: '458', 61: '145', 62: '1458', 63: '1', 64: '2', 65: '7', 66: '68', 67: '568', 68: '4568', 69: '9', 70: '3', 71: '4568', 72: '8', 73: '45', 74: '9', 75: '136', 76: '156', 77: '13456', 78: '7', 79: '2', 80: '1456'}
n = 9
sb_height = 3
sb_width = 3
symbol_set = find_symbolset()
constraint_set = find_constraintset()
neighbors = find_neighbors()
symbol_dict = find_symbolsFrequency
assign(board, 6, 6)
print(forward_looking(board, {6}))

