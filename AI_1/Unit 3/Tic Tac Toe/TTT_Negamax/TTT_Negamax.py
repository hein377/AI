import sys
import random

#Global Variables
size = 3
board = ""
playersymbol = {}

def is_empty(board):
    if(len(s:=set(board)) == 1 and s.pop() == "."): return True
    return False

def printboard(board):
    for i in range(len(board)):
        if((i+1)%3 == 0): print(board[i] + "    %s%s%s" % (i-2, i-1, i))
        else: print(board[i], end = "")
    print()

def setcharAt(board, index, ch):
    print()
    temp = list(board)
    temp[index] = ch
    return ''.join(temp)

def score(winningsymbol, cplayersymbol):
    if(winningsymbol == cplayersymbol): return 1
    return -1

def game_over(board, cplayersymbol):           #returns 1 if current player determined by second parameter wins, 0 if tie, -1 if other player wins
    hc, vc, dc = horizontal_check(board), vertical_check(board), diagonal_check(board)
    if(hc != None): return score(hc, cplayersymbol)
    if(vc != None): return score(vc, cplayersymbol)
    if(dc != None): return score(dc, cplayersymbol)
    if("." not in board): return 0
    return None

def horizontal_check(board):
    global size 
    for i in range(0, len(board), size):
        if(board[i] != "." and board[i] == board[i+1] == board[i+2]): return board[i]
    return None

def vertical_check(board):
    for i in range(size):
        if (board[i] != "." and board[i] == board[i+size] == board[i+size+size]): return board[i]
    return None

def diagonal_check(board):
    if(board[2] != "." and board[2] == board[4] == board[6]): return board[2]
    elif(board[0] != "." and board[0] == board[4] == board[8]): return board[0]
    return None

def possible_next_boards(board, player):            #{board : index}
    pos_boards = {}
    for i in range(len(board)):
        temp_board = list(board)
        if(board[i] == "."): 
            temp_board[i] = player
            pos_boards.update({(''.join(temp_board)) : i})
    return pos_boards

def othersymbol(symbol):
    if(symbol == "X"): return "O"
    elif(symbol == "O"): return "X"
    return None

def negamax(board, cplayersymbol):
    if((score:=game_over(board, cplayersymbol)) != None): return score         #if the game is over, return the score based on the currentplayer determined by cplayersymbol
    results = []
    for next_board in possible_next_boards(board, cplayersymbol).keys():        #for the possible future boards (based cplayer's turn)
        results.append(-negamax(next_board, othersymbol(cplayersymbol)))        #append the negative value of their return value since players are swapped and the value is based on player's turn
    return max(results)                                                         #always return the max of possible values since 1 means cp win and we assume perfect play by opponent

def getboardsfuture(board):             #{index : (1, 0, or -1)}
    posnextboards = possible_next_boards(board, playersymbol["cp"])
    boardsfuture = {}
    for next_boards in posnextboards.keys():
        ind = posnextboards[next_boards]
        boardsfuture.update({ind: -negamax(next_boards, playersymbol["p"])})
    return boardsfuture

def addtodic(dic, key, val):
    if(key not in dic): dic.update({key:[val]})
    else: dic[key].append(val)

def makechoice(dic):
    if("win" in dic): return random.choice(dic["win"])
    if("tie" in dic): return random.choice(dic["tie"])
    if("loss" in dic): return random.choice(dic["loss"])
    return None

def computer():
    global board
    print("Current board:")
    printboard(board)
    states, boardsfuture = {}, getboardsfuture(board)                                             # states = {"win" : [indices], "tie" : [indices], "loss" : [indices]}
    for ind in boardsfuture.keys():
        if((future:=boardsfuture[ind]) == 1): result = "win"
        elif(future == 0): result = "tie"
        elif(future == -1): result = "loss"
        addtodic(states, result, ind)
        print("Moving at %s results in a %s" % (ind, result))
    print("\nI choose space %s." % (choice:=makechoice(states)))
    board = setcharAt(board, choice, playersymbol["cp"])

def player():
    global board
    print("Current board:")
    printboard(board)
    print("You can move to any of these spaces: %s." % ', '.join([str(i) for i in range(len(board)) if board[i] == "."]))
    index = int(input("Your choice? "))
    board = setcharAt(board, index, playersymbol["p"])

def countsymbol(board, symbol):
    count = 0
    for i in range(len(board)):
        if(board[i] == symbol): count += 1
    return count

board = sys.argv[1]
if(board == "........."):           #Enters a blank board
    answer, board = input("Should I be X or O? "), "........."
    print()
    if(answer == "O"): 
        playersymbol = {"p":"X", "cp":"O"}
        while((game_over(board, playersymbol["cp"])) == None):
            player()
            if((game_over(board, playersymbol["cp"])) == None): computer()
    elif(answer == "X"):
        playersymbol = {"p":"O", "cp":"X"}
        while((game_over(board, playersymbol["cp"])) == None):
            computer()
            if((game_over(board, playersymbol["cp"])) == None): player()
else:                               #Enters premade board
    if(countsymbol(board, "X") == countsymbol(board, "O")): playersymbol = {"p":"O", "cp":"X"}
    else: playersymbol = {"p":"X", "cp":"O"}
    while((game_over(board, playersymbol["cp"])) == None):
        computer()
        if((game_over(board, playersymbol["cp"])) == None): player()

printboard(board)
x = game_over(board, playersymbol["cp"])
if(x == 1): print("I win!")
elif(x == -1): print("You win!")
elif(x == 0): print("We tied!")