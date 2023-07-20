import sys
import random

#Global Variables
size = 3

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

def game_over(board):
    (hc, winner1), (vc, winner2), (dc, winner3) = horizontal_check(board), vertical_check(board), diagonal_check(board)
    if(hc):
        if(winner1 == "X"): return 1
        elif(winner1 == "O"): return -1
    elif(vc):
        if(winner2 == "X"): return 1
        elif(winner2 == "O"): return -1
    elif(dc):
        if(winner3 == "X"): return 1
        elif(winner3 == "O"): return -1
    elif("." not in board): return 0
    return None

def horizontal_check(board):
    global size 
    for i in range(0, len(board), size):
        if (board[i] == board[i+1] == board[i+2]): return True, board[i]
    return False, None

def vertical_check(board):
    for i in range(size):
        if (board[i] == board[i+size] == board[i+size+size]): return True, board[i]
    return False, None

def diagonal_check(board):
    if(board[2] == board[4] == board[6]): return True, board[2]
    elif(board[0] == board[4] == board[8]): return True, board[0]
    return False, None

def possible_next_boards(board, player):            #{board : index}
    pos_boards = {}
    for i in range(len(board)):
        temp_board = list(board)
        if(board[i] == "."): 
            temp_board[i] = player
            pos_boards.update({(''.join(temp_board)) : i})
    return pos_boards

def otherplayer(cplayer):
    if(cplayer == "cp"): return "p"
    elif(cplayer == "p"): return "cp"
    return None

def max_step(board, player):                                                    #returns 1, 0, or -1
    if((score:=game_over(board)) != None): return score
    results = []
    for next_board in possible_next_boards(board, playersymbol[player]).keys():
        results.append(min_step(next_board, otherplayer(player)))
    return max(results)

def min_step(board, player):                                                    #returns 1, 0, or -1
    if((score:=game_over(board)) != None): return score
    results = []
    for next_board in possible_next_boards(board, playersymbol[player]).keys():
        results.append(max_step(next_board, otherplayer(player)))
    return min(results)

def getboardsfuturecpX(board):             #{index : (1, 0, or -1)}
    posnextboards = possible_next_boards(board, playersymbol["cp"])
    boardsfuture = {}
    for next_boards in posnextboards.keys():
        ind = posnextboards[next_boards]
        boardsfuture.update({ind: min_step(next_boards, "p")})
    return boardsfuture

def getboardsfuturecpO(board):             #{index : (1, 0, or -1)}
    posnextboards = possible_next_boards(board, playersymbol["cp"])
    boardsfuture = {}
    for next_boards in posnextboards.keys():
        ind = posnextboards[next_boards]
        boardsfuture.update({ind: max_step(next_boards, "p")})
    return boardsfuture

def game(x):
    print("Current board:")
    printboard(board)
    if(x == 0): print("We tied!")
    elif(playersymbol["cp"] == "X"):
        if(x == 1): print("I win!")
        if(x == -1): print("You win!")
    elif(playersymbol["cp"] == "O"):
        if(x == -1): print("I win!")
        if(x == 1): print("You win!")

def player():
    global board
    print("Current board:")
    printboard(board)
    print("You can move to any of these spaces: %s." % ', '.join([str(i) for i in range(len(board)) if board[i] == "."]))
    index = int(input("Your choice? "))
    board = setcharAt(board, index, playersymbol["p"])

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
    states = {}                                             # {"win" : [indices], "tie" : [indices], "loss" : [indices]}
    if(playersymbol["cp"] == "X"): 
        boardsfuture = getboardsfuturecpX(board)
        for ind in boardsfuture.keys():
            if((future:=boardsfuture[ind]) == 1): result = "win"
            elif(future == 0): result = "tie"
            elif(future == -1): result = "loss"
            addtodic(states, result, ind)
            print("Moving at %s results in a %s" % (ind, result))
        print("\nI choose space %s." % (choice:=makechoice(states)))
    elif(playersymbol["cp"] == "O"): 
        boardsfuture = getboardsfuturecpO(board)
        for ind in boardsfuture.keys():
            if((future:=boardsfuture[ind]) == 1): result = "loss"
            elif(future == 0): result = "tie"
            elif(future == -1): 
                result = "win"
            addtodic(states, result, ind)
            print("Moving at %s results in a %s" % (ind, result))
        print("\nI choose space %s." % (choice:=makechoice(states)))
    board = setcharAt(board, choice, playersymbol["cp"])

def countsymbol(board, symbol):
    count = 0
    for i in range(len(board)):
        if(board[i] == symbol): count += 1
    return count


x = -999
board = sys.argv[1]
if(board == "........."):
    answer = input("Should I be X or O? ")
    print()
    if(answer == "O"): 
        playersymbol = {"p":"X", "cp":"O"}
        while((x:=game_over(board)) != 1 and x != 0 and x != -1):
            player()
            if((x:=game_over(board)) != 1 and x != 0 and x != -1): computer()
    elif(answer == "X"):
        playersymbol = {"p":"O", "cp":"X"}
        while((x:=game_over(board)) != 1 and x != 0 and x != -1):
            computer()
            if((x:=game_over(board)) != 1 and x != 0 and x != -1): player()
    game(x)
else:
    if(countsymbol(board, "X") == countsymbol(board, "O")): playersymbol = {"p":"O", "cp":"X"}
    else: playersymbol = {"p":"X", "cp":"O"}
    while((x:=game_over(board)) != 1 and x != 0 and x != -1):
        computer()
        if((x:=game_over(board)) != 1 and x != 0 and x != -1): player()
    game(x)