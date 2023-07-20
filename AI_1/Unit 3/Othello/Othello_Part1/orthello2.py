import sys
import time
import math

#Global Variables
inputboard = ""
normaltobordered = {}
borderedtonormal = {}
board_nextinds = {}         #{board : posnextinds}

#possible_moves
def indconversion():
    global normaltobordered, borderedtonormal
    for i in range(64): 
        normaltobordered.update({i : (converted:=(i + 11 + ((i//8) * 2)))})
        borderedtonormal.update({converted : i})
indconversion()

def border(board):                      #returns a string of the board surrounded by "!"
    temp = ""
    for i in range(0, 57, 8): temp += "!" + board[i:i+8] + "!"
    return "!!!!!!!!!!" + temp + "!!!!!!!!!!"

def printboard(board):
    for i in range(0, 57, 8):
        print(board[i:i+8])

def printborderedboard(board):
    for i in range(0, 91, 10):
        print(board[i:i+10])

def othertoken(token):
    if(token == "x"): return "o"
    if(token == "o"): return "x"
    return None

def addtodic(dic, key, val):
    if(key not in dic): dic.update({key : [val]})
    else: dic[key].append(val)

def getsurroundingindices(ind):         #returns [surrounding indices]
    return [ind-1, ind+1, ind-10, ind+10, ind-11, ind-9, ind+9, ind+11]

def add_surrounding_indices(dic, board, ind):          #given an index, check for blank indexes 1 space around the index and add them to set s
    for i in getsurroundingindices(ind):
        if(board[i] == "."): addtodic(dic, ind, i)

def getneighbors(board, borderedboard, token):         #normal board
    neighbors = {}                      #neighbors = {token's index : [indices of blank spaces next to token]}
    for i in range(len(board)):
        if(board[i] == token): 
            add_surrounding_indices(neighbors, borderedboard, normaltobordered[i])
    return neighbors

def checktoken(ind, tokenind, board, token):                #checks if token is valid
    add_by, cur_ind = (tokenind - ind), tokenind
    while(board[cur_ind] == token): cur_ind += add_by
    if(board[cur_ind] == othertoken(token)): return True
    return False

def possible_moves(board, token):       #return all possible moves at token's turn
    bordered_board, possible_moves, other_token = border(board), [], othertoken(token)
    neighbors = getneighbors(board, bordered_board, other_token)         #neighbors = {other token's index : [indices of blank spaces next to token]}
    for othertokenind in neighbors.keys():
        possibleinds = neighbors[othertokenind]
        for possibleind in possibleinds:
            if(checktoken(possibleind, othertokenind, bordered_board, other_token) and (possibleind not in possible_moves)): possible_moves.append(possibleind)
    for i in range(len(possible_moves)):
        borderedind = possible_moves[i]
        possible_moves[i] = borderedtonormal[borderedind]
    return possible_moves

#make_move
def check_surroundings(board, token, ind):                  #returns adjacent indices w/ other token
    surrounding_indices, surrounding_tokeninds = getsurroundingindices(ind), []
    for ind in surrounding_indices:
        if(board[ind] == token): surrounding_tokeninds.append(ind)
    return surrounding_tokeninds

def make_move(board, token, index):         #returns new board with token placed at index and other token's pieces flipped
    bordered_board, borderedindex, newboard, other_token = border(board), normaltobordered[index], list(board), othertoken(token)
    surrounding_other_token_inds = check_surroundings(bordered_board, other_token, borderedindex)
    for othertokenind in surrounding_other_token_inds:
        path, addby, cur_ind = [index], (othertokenind - borderedindex), othertokenind
        while(bordered_board[cur_ind] == other_token):
            path.append(borderedtonormal[cur_ind])
            cur_ind += addby
        if(bordered_board[cur_ind] == token):
            for ind in path: newboard[ind] = token
    return ''.join(newboard)

#Score_function
def corners(board):
    corners, score = [0, 7, 56, 63], 0
    for ind in corners:
        if(board[ind] == "x"): score += 1000
        if(board[ind] == "o"): score -= 1000
    return score

def near_corners(board):
    near_corners, score = [1, 6, 8, 9, 14, 15, 48, 49, 54, 55, 57, 62], 0
    for ind in near_corners:
        if(board[ind] == "x"): score -= 250
        if(board[ind] == "o"): score += 250
    return score

def completerowcol(board):
    i, score, row, col = 0, 0, {0, 1, 2, 3, 4, 5, 6, 7}, {0, 1, 2, 3, 4, 5, 6, 7}
    while(i<64 and (len(row) != 0 or len(col) != 0)):
        if(board[i] == "."):
            row.discard(i/8)
            col.discard(i%8)
        i+=1
    for i in row:
        if(board[i] == "x"): score += 750
        if(board[i] == "o"): score -= 750
    for i in col:
        if(board[i] == "x"): score += 750
        if(board[i] == "o"): score -= 750
    return score

def mobility(board):
    if(board in board_nextinds): posmoves = board_nextinds[board]
    else: posmoves = possible_moves(board, "x")
    return 45*(len(posmoves) - len(possible_moves(board, "o")))

def game(board, gm):
    if(gm):
        countx, counto = 0, 0
        for token in board:
            if(token == "x"): countx += 1
            if(token == "o"): counto += 1
        return 100000 * (countx - counto)
    return 0

def scoreboard(board, gm):
    return game(board, gm) + corners(board) + near_corners(board) + completerowcol(board) + mobility(board)

#Minimax
def gameover(board, token):
    if("." not in board): return True
    return len(possible_moves(board, token)) == 0

def max_step(board, alpha, beta, token, depth):
    if(gameover(board, token)): return scoreboard(board, True)
    if(depth == 1): return scoreboard(board, False)
    results = []
    if board in board_nextinds.keys(): posmoves = board_nextinds[board]
    else: board_nextinds.update({board : (posmoves:=possible_moves(board, token))})
    for next_ind in posmoves:
        s = min_step(make_move(board, token, next_ind), alpha, beta, othertoken(token), depth-1)
        if(s > alpha): alpha = s
        if(alpha >= beta): return s
        results.append(s)
    return max(results)

def min_step(board, alpha, beta, token, depth):
    if(gameover(board, token)): return scoreboard(board, True)
    if(depth == 1): return scoreboard(board, False)
    results = []
    if board in board_nextinds.keys(): posmoves = board_nextinds[board]
    else: board_nextinds.update({board : (posmoves:=possible_moves(board, token))})
    for next_ind in posmoves:
        s = max_step(make_move(board, token, next_ind), alpha, beta, othertoken(token), depth-1)
        if(s < beta): beta = s
        if(alpha >= beta): return s
        results.append(s)
    return min(results)

#find_next_move
def find_next_move(board, token, depth):
    posboards = {i : make_move(board, token, i) for i in possible_moves(board, token)}
    if(token == "x"):
        maxscore, maxind = -math.inf, 0
        for i, nextboard in posboards.items():
            score = min_step(nextboard, -math.inf, math.inf, "o", depth)
            if(score > maxscore):
                maxscore = score
                maxind = i
        return maxind
    elif(token == "o"): 
        minscore, minind = math.inf, 0
        for i, nextboard in posboards.items():
            score = max_step(nextboard, -math.inf, math.inf, "x", depth)
            if(score < minscore):
                minscore = score
                minind = i
        return minind
    return 0

board = sys.argv[1]
player = sys.argv[2]
depth = 1
for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
   print(find_next_move(board, player, depth))
   depth += 1