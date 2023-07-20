#Global varaibles
from turtle import pos


normaltobordered = {}
borderedtonormal = {}

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

def getneighbors(board, token):
    neighbors = {}                      #neighbors = {token's index : [indices of blank spaces next to token]}
    for x in range(11, 82, 10):
        for i in range(x, x+8):
            if(board[i] == token): add_surrounding_indices(neighbors, board, i)
    return neighbors

def checktoken(ind, tokenind, board, token):                #checks if token is valid
    add_by, cur_ind = (tokenind - ind), tokenind
    while(board[cur_ind] == token): cur_ind += add_by
    if(board[cur_ind] == othertoken(token)): return True
    return False

def possible_moves(board, token):       #return all possible moves at token's turn
    bordered_board, possible_moves, other_token = border(board), [], othertoken(token)
    neighbors = getneighbors(bordered_board, other_token)         #neighbors = {other token's index : [indices of blank spaces next to token]}
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

board = "...........................ox......xxx.........................."
token = "o"
posboards = {i : make_move(board, token, i) for i in possible_moves(board, token)}
print(posboards)