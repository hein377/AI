import random
import pickle

from pip import main
NUM_TRIALS = 5
POPULATION_SIZE = 200
NUM_CLONES = 40
TOURNAMENT_SIZE = 30
TOURNAMENT_WIN_PROBABILITY = .75
MUTATION_RATE = .1
STRATEGY_LIST_SIZE = 6
board = ""
for x in range(0, 200): board += " "
def findTopBlocks(board):
    tops = []
    for x in range(0, 10):
        pos = x
        for y in range(0, 20):
            if board[pos] == "#" and pos not in tops: 
                tops.append(pos)
                break
            pos += 10
        if pos not in tops: tops.append(pos)
    return tops
def findIOrientations(board, top, gameOvers):
    orientations = set()
    count = 0
    for x in top:
        if count <= 6:
            if x - 10 < 0: gameOvers += 1
            elif board[x-10] != '#' and board[x-9] != '#' and board[x-8] != '#' and board[x-7] != '#': orientations.add(board[0:x-10]+"####"+board[x-6:])
        if count <= 7 and count >= 1: 
            if x - 11 < 0: gameOvers += 1
            elif board[x-11] != '#' and board[x-10] != '#' and board[x-9] != '#' and board[x-8] != '#': orientations.add(board[0:x-11]+"####"+board[x-7:])
        if count <= 8 and count >= 2: 
            if x - 12 < 0: gameOvers += 1
            elif board[x-12] != '#' and board[x-11] != '#' and board[x-10] != '#' and board[x-9] != '#': orientations.add(board[0:x-12]+"####"+board[x-8:])
        if count >= 3: 
            if x - 13 < 0: gameOvers += 1
            elif board[x-13] != '#' and board[x-12] != '#' and board[x-11] != '#' and board[x-10] != '#': orientations.add(board[0:x-13]+"####"+board[x-9:]) 
        if x - 10 < 0 or x - 20 < 0 and x - 30 < 0 or x - 40 < 0: gameOvers += 1
        elif board[x-10] != '#' and board[x-20] != '#' and board[x-30] != '#' and board[x-40] != '#': orientations.add(board[0:x-40]+"#"+board[x-39:x-30]+"#"+board[x-29:x-20]+"#"+board[x-19:x-10]+"#"+board[x-9:])
        count += 1
    return [orientations, gameOvers]

def findOOrientations(board, top, gameOvers):
    orientations = set()
    count = 0
    for x in top: 
        if count <= 8: 
            if x - 10 < 0 or x - 20 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-20] !='#' and board[x-9] !='#' and board[x-19] !='#': orientations.add(board[0:x-20]+"##"+board[x-18:x-10]+"##"+board[x-8:])
        if count >= 1: 
            if x - 11 < 0 or x - 21 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-20] !='#' and board[x-11] !='#' and board[x-21] !='#': orientations.add(board[0:x-21]+"##"+board[x-19:x-11]+"##"+board[x-9:])
        count += 1
    return [orientations, gameOvers]

def findTOrientations(board, top, gameOvers):
    orientations = set()
    count = 0
    for x in top:
        if count <= 7: 
            if x - 10 < 0 or x - 19 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-9] !='#' and board[x-8] !='#' and board[x-19] !='#': orientations.add(board[0:x-19]+"#"+board[x-18:x-10]+"###"+board[x-7:])
        if count <= 8 and count >= 1: 
            if x - 11 < 0 or x - 20 < 0: gameOvers += 1
            elif board[x-11] !='#' and board[x-10] !='#' and board[x-9] !='#' and board[x-20] !='#': orientations.add(board[0:x-20]+"#"+board[x-19:x-11]+"###"+board[x-8:])
        if count >= 2: 
            if x - 12 < 0 or x - 21 < 0: gameOvers += 1
            elif board[x-12] !='#' and board[x-11] !='#' and board[x-10] !='#' and board[x-21] !='#': orientations.add(board[0:x-21]+"#"+board[x-20:x-12]+"###"+board[x-9:])
        if count <= 8: 
            if x - 10 < 0 or x - 20 < 0 and x - 30 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-20] !='#' and board[x-30] !='#' and board[x-19] !='#': orientations.add(board[0:x-30]+"#"+board[x-29:x-20]+"##"+board[x-18:x-10]+"#"+board[x-9:])
        if count >= 1 and x - 1 >= 0 and x - 1 <= 199: 
            if x - 11 < 0 or x - 21 < 0: gameOvers += 1
            elif board[x-1] !='#' and board[x-11] !='#' and board[x-10] !='#' and board[x-21] !='#': orientations.add(board[0:x-21]+"#"+board[x-20:x-11]+"##"+board[x-9:x-1]+"#"+board[x:])
        if count <= 7 and x + 1 <= 199: 
            if x - 10 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-9] !='#' and board[x-8] !='#' and board[x+1] !='#': orientations.add(board[0:x-10]+"###"+board[x-7:x+1]+"#"+board[x+2:])
        if count <= 8 and count >= 1: 
            if x - 10 < 0 or x - 21 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-21] !='#' and board[x-20] !='#' and board[x-19] !='#': orientations.add(board[0:x-21]+"###"+board[x-18:x-10]+"#"+board[x-9:])
        if count >= 2 and x - 1 >= 0 and x - 1 <= 199: 
            if x - 12 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-11] !='#' and board[x-12] !='#' and board[x-1] !='#': orientations.add(board[0:x-12]+"###"+board[x-9:x-1]+"#"+board[x:])
        if count <= 8 and x + 1 <= 199: 
            if x - 9 < 0 or x - 10 < 0 or x - 19 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-9] !='#' and board[x-19] !='#' and board[x+1] !='#': orientations.add(board[0:x-19]+"#"+board[x-18:x-10]+"##"+board[x-8:x+1]+"#"+board[x+2:])
        if count >= 1: 
            if x - 10 < 0 or x - 30 < 0 or x - 21 < 0: gameOvers += 1 
            elif board[x-10] !='#' and board[x-21] !='#' and board[x-20] !='#' and board[x-30] !='#': orientations.add(board[0:x-30]+"#"+board[x-29:x-21]+"##"+board[x-19:x-10]+"#"+board[x-9:])
        count += 1
    return [orientations, gameOvers]

def findSOrientations(board, top, gameOvers):
    orientations = set()
    count = 0
    for x in top:
        if count <= 7: 
            if x - 10 < 0 or x - 19 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-9] !='#' and board[x-19] !='#' and board[x-18] !='#': orientations.add(board[0:x-19]+"##"+board[x-17:x-10]+"##"+board[x-8:])
        if count <= 8 and count >= 1: 
            if x - 11 < 0 or x - 20 < 0: gameOvers += 1
            elif board[x-11] !='#' and board[x-10] !='#' and board[x-20] !='#' and board[x-19] !='#': orientations.add(board[0:x-20]+"##"+board[x-18:x-11]+"##"+board[x-9:])
        if count >= 2 and x - 2 >= 0 and x - 2 <= 199: 
            if x - 11 < 0: gameOvers += 1
            elif board[x-11] !='#' and board[x-10] !='#' and board[x-2] !='#' and board[x-1] !='#': orientations.add(board[0:x-11]+"##"+board[x-9:x-2]+"##"+board[x:])
        if count <= 8 and x + 1 <= 199: 
            if x - 10 < 0 or x - 20 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-9] !='#' and board[x-20] !='#' and board[x+1] !='#': orientations.add(board[0:x-20]+"#"+board[x-19:x-10]+"##"+board[x-8:x+1]+"#"+board[x+2:])
        if count >= 1: 
            if x - 10 < 0 or x - 21 < 0 or x - 31 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-21] !='#' and board[x-20] !='#' and board[x-31] !='#': orientations.add(board[0:x-31]+"#"+board[x-30:x-21]+"##"+board[x-19:x-10]+"#"+board[x-9:])
        count += 1
    return [orientations, gameOvers]

def findZOrientations(board, top, gameOvers):
    orientations = set()
    count = 0
    for x in top:
        if count <= 7 and x + 2 <= 199: 
            if x - 10 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-9] !='#' and board[x+1] !='#' and board[x+2] !='#': orientations.add(board[0:x-10]+"##"+board[x-8:x+1]+"##"+board[x+3:])
        if count <= 8 and count >= 1: 
            if x - 10 < 0 or x - 21 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-9] !='#' and board[x-21] !='#' and board[x-20] !='#': orientations.add(board[0:x-21]+"##"+board[x-19:x-10]+"##"+board[x-8:])
        if count >= 2: 
            if x - 11 < 0 or x - 22 < 0: gameOvers += 1
            elif board[x-11] !='#' and board[x-10] !='#' and board[x-22] !='#' and board[x-21] !='#': orientations.add(board[0:x-22]+"##"+board[x-20:x-11]+"##"+board[x-9:])
        if count <= 8: 
            if x - 10 < 0 or x - 20 < 0 or x - 29 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-20] !='#' and board[x-19] !='#' and board[x-29] !='#': orientations.add(board[0:x-29]+"#"+board[x-28:x-20]+"##"+board[x-18:x-10]+"#"+board[x-9:])
        if count >= 1 and x - 1 >= 0 and x - 1 <= 199: 
            if x - 11 < 0 or x - 20 < 0: gameOvers += 1
            elif board[x-1] !='#' and board[x-10] !='#' and board[x-11] !='#' and board[x-20] !='#': orientations.add(board[0:x-20]+"#"+board[x-19:x-11]+"##"+board[x-9:x-1]+"#"+board[x:])
        count += 1
    return [orientations, gameOvers]

def findJOrientations(board, top, gameOvers):
    orientations = set()
    count = 0
    for x in top:
        if count <= 7: 
            if x - 10 < 0 or x - 20 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-20] !='#' and board[x-9] !='#' and board[x-8] !='#': orientations.add(board[0:x-20]+"#"+board[x-19:x-10]+"###"+board[x-7:])
        if count <= 8 and count >= 1: 
            if x - 11 < 0 or x - 21 < 0: gameOvers += 1
            elif board[x-11] !='#' and board[x-21] !='#' and board[x-10] !='#' and board[x-9] !='#': orientations.add(board[0:x-21]+"#"+board[x-20:x-11]+"###"+board[x-8:])
        if count >= 2: 
            if x - 12 < 0 or x - 22 < 0: gameOvers += 1
            elif board[x-12] !='#' and board[x-22] !='#' and board[x-11] !='#' and board[x-10] !='#': orientations.add(board[0:x-22]+"#"+board[x-21:x-12]+"###"+board[x-9:])
        if count <= 8: 
            if x - 10 < 0 or x - 20 < 0 or x - 30 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-20] !='#' and board[x-30] !='#' and board[x-29] !='#': orientations.add(board[0:x-30]+"##"+board[x-28:x-20]+"#"+board[x-19:x-10]+"#"+board[x-9:])
        if count >= 1 and x - 1 >= 0 and x + 9 <= 199: 
            if x - 11 < 0: gameOvers += 1
            elif board[x-11] !='#' and board[x-10] !='#' and board[x-1] !='#' and board[x+9] !='#': orientations.add(board[0:x-11]+"##"+board[x-9:x-1]+"#"+board[x:x+9]+"#"+board[x+10:])
        if count <= 7 and x + 2 <= 199: 
            if x - 10 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-9] !='#' and board[x-8] !='#' and board[x+2] !='#': orientations.add(board[0:x-10]+"###"+board[x-7:x+2]+"#"+board[x+3:])
        if count <= 8 and count >= 1 and x + 1 <= 199: 
            if x - 11 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-9] !='#' and board[x-11] !='#' and board[x+1] !='#': orientations.add(board[0:x-11]+"###"+board[x-8:x+1]+"#"+board[x+2:])
        if count >= 2: 
            if x - 10 < 0 or x - 22 < 0: gameOvers += 1
            elif board[x-22] !='#' and board[x-21] !='#' and board[x-20] !='#' and board[x-10] !='#': orientations.add(board[0:x-22]+"###"+board[x-19:x-10]+"#"+board[x-9:])
        if count <= 8: 
            if x - 10 < 0 or x - 19 < 0 or x - 29 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-9] !='#' and board[x-19] !='#' and board[x-29] !='#': orientations.add(board[0:x-29]+"#"+board[x-28:x-19]+"#"+board[x-18:x-10]+"##"+board[x-8:])
        if count >= 1: 
            if x - 11 < 0 or x - 20 < 0 or x - 30 < 0: gameOvers += 1
            elif board[x-11] !='#' and board[x-10] !='#' and board[x-20] !='#' and board[x-30] !='#': orientations.add(board[0:x-30]+"#"+board[x-29:x-20]+"#"+board[x-19:x-11]+"##"+board[x-9:])
        count += 1
    return [orientations, gameOvers]

def findLOrientations(board, top, gameOvers):
    orientations = set()
    count = 0
    for x in top:
        if count <= 7: 
            if x - 10 < 0 or x - 18 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-9] !='#' and board[x-8] !='#' and board[x-18] !='#': orientations.add(board[0:x-18]+"#"+board[x-17:x-10]+"###"+board[x-7:])
        if count <= 8 and count >= 1: 
            if x - 11 < 0 or x - 19 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-9] !='#' and board[x-11] !='#' and board[x-19] !='#': orientations.add(board[0:x-19]+"#"+board[x-18:x-11]+"###"+board[x-8:])
        if count >= 2: 
            if x - 12 < 0 or x - 20 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-12] !='#' and board[x-11] !='#' and board[x-20] !='#': orientations.add(board[0:x-20]+"#"+board[x-19:x-12]+"###"+board[x-9:])
        if count <= 8:
            if x - 10 < 0 or x - 20 < 0 or x - 30 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-20] !='#' and board[x-30] !='#' and board[x-9] !='#':  orientations.add(board[0:x-30]+"#"+board[x-29:x-20]+"#"+board[x-19:x-10]+"##"+board[x-8:])
        if count >= 1: 
            if x - 11 < 0 or x - 21 < 0 or x - 31 < 0: gameOvers += 1
            elif board[x-11] !='#' and board[x-21] !='#' and board[x-31] !='#' and board[x-10] !='#': orientations.add(board[0:x-31]+"#"+board[x-30:x-21]+"#"+board[x-20:x-11]+"##"+board[x-9:])
        if count <= 7: 
            if x - 10 < 0 or x - 20 < 0: gameOvers += 1
            elif board[x-20] !='#' and board[x-19] !='#' and board[x-18] !='#' and board[x-10] !='#': orientations.add(board[0:x-20]+"###"+board[x-17:x-10]+"#"+board[x-9:])
        if count <= 8 and count >= 1 and x - 1 >= 0 and x - 1 <= 199: 
            if x - 11 < 0: gameOvers += 1
            elif board[x-11] !='#' and board[x-10] !='#' and board[x-9] !='#' and board[x-1] !='#': orientations.add(board[0:x-11]+"###"+board[x-8:x-1]+"#"+board[x:])
        if count >= 2 and x - 2 >= 0 and x - 2 <= 199: 
            if x - 10 < 0: gameOvers += 1
            elif board[x-12] !='#' and board[x-11] !='#' and board[x-10] !='#' and board[x-2] !='#': orientations.add(board[0:x-12]+"###"+board[x-9:x-2]+"#"+board[x-1:])
        if count <= 8 and x + 1 <= 199 and x + 11 <= 199: 
            if x - 10 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-9] !='#' and board[x+1] !='#' and board[x+11] !='#': orientations.add(board[0:x-10]+"##"+board[x-8:x+1]+"#"+board[x+2:x+11]+"#"+board[x+12:])
        if count >= 1: 
            if x - 10 < 0 or x - 20 < 0 or x - 31 < 0: gameOvers += 1
            elif board[x-10] !='#' and board[x-20] !='#' and board[x-30] !='#' and board[x-31] !='#': orientations.add(board[0:x-31]+"##"+board[x-29:x-20]+"#"+board[x-19:x-10]+"#"+board[x-9:])
        count += 1
    return [orientations, gameOvers]

def transform(board):
    count = 0
    clears = 0
    for x in range(0, 20):
        if " " not in board[count:count+10]: 
            board = "          " + board[0:count]+board[count+10:]
            clears += 1
        count += 10
    return [board, clears]

def heuristic(board, strategy, cl):
    highestColumnHeight = 0
    deepestWellDepth = 0
    holes = 0
    lineClears = cl
    bumpiness = 0
    sumOfHeights = 0
    tops = findTopBlocks(board)
    

    for x in range(1, len(tops)): bumpiness += abs((20 - (int(tops[x] / 10))) - (20 - (int(tops[x-1] / 10))))
    for x in tops:
        sumOfHeights += (20 - int(x / 10))
        if (20 - int(x / 10)) > highestColumnHeight: highestColumnHeight = (20 - int(x / 10))
        if int(x / 10) > deepestWellDepth: deepestWellDepth = int(x / 10)
    for x in range(10, 200):
        if board[x] == " " and board[x-10] == "#": holes += 1
    a, b, c, d, e, f = strategy # As many variables as you want!
    value = 0
    value += float(a) * float(highestColumnHeight)
    value += float(b) * float(deepestWellDepth)
    value += float(c) * float(holes)
    value += float(d) * float(lineClears)
    value += float(e) * float(bumpiness)
    value += float(f) * float(sumOfHeights)
    # add as many variables as you want - whatever you think might be relevant!
    return value

def play_game(board, strategy):
    points = 0
    pieces = ["I", "Z", "O", "L", "J", "S", "T"]
    b = False
    while not b:
        piece = random.choice(pieces)
        top = findTopBlocks(board)
        if piece == "I": o = findIOrientations(board, top, 0)
        if piece == "Z": o = findZOrientations(board, top, 0)
        if piece == "O": o = findOOrientations(board, top, 0)
        if piece == "L": o = findLOrientations(board, top, 0)
        if piece == "J": o = findJOrientations(board, top, 0)
        if piece == "S": o = findSOrientations(board, top, 0)
        if piece == "T": o = findTOrientations(board, top, 0)
        for boards in o:
            for b in boards:
                print(b)
                print(printboard(b))
                input()
        if len(o[0]) == 0: b = True
        else:
            max2 = dict()
            tInt = transform(list(o[0])[0])
            highestScore = heuristic(tInt[0], strategy, tInt[1])
            for orientation in list(o[0]):
                t = transform(orientation)
                poss_score = heuristic(t[0], strategy, t[1])
                if highestScore <= poss_score: highestScore = poss_score
                max2[poss_score] = [t[0], t[1]]
                # Keep track of the board with the highest heuristic score however you like!
            board = max2[highestScore][0]
            cl = max2[highestScore][1]
            if cl > 0:
                if cl == 1: new_points = 40
                if cl == 2: new_points = 100
                if cl == 3: new_points = 300
                if cl == 4: new_points = 1200
                points += new_points 
            #reminder: 1 row cleared --> 40 points, 2 --> 100, 3 --> 300, 4 --> 1200
    return points

def play_gameWithDisplay(board, strategy, p):
    points = 0
    pieces = ["I", "Z", "O", "L", "J", "S", "T"]
    b = False
    while not b:
        piece = random.choice(pieces)
        top = findTopBlocks(board)
        if piece == "I": o = findIOrientations(board, top, 0)
        if piece == "Z": o = findZOrientations(board, top, 0)
        if piece == "O": o = findOOrientations(board, top, 0)
        if piece == "L": o = findLOrientations(board, top, 0)
        if piece == "J": o = findJOrientations(board, top, 0)
        if piece == "S": o = findSOrientations(board, top, 0)
        if piece == "T": o = findTOrientations(board, top, 0)
        if len(o[0]) == 0: b = True
        else:
            max2 = dict()
            tInt = transform(list(o[0])[0])
            highestScore = heuristic(tInt[0], strategy, tInt[1])
            for orientation in list(o[0]):
                t = transform(orientation)
                poss_score = heuristic(t[0], strategy, t[1])
                if highestScore <= poss_score: highestScore = poss_score
                max2[poss_score] = [t[0], t[1]]
                # Keep track of the board with the highest heuristic score however you like!
            board = max2[highestScore][0]
            cl = max2[highestScore][1]
            if cl > 0:
                if cl == 1: new_points = 40
                if cl == 2: new_points = 100
                if cl == 3: new_points = 300
                if cl == 4: new_points = 1200
                points += new_points 
            print("=======================")
            count = 0
            for x in range(0, 20):
                s = "| "
                for x2 in board[count:count+10]: s += str(x2) + " "
                s += "|"
                print(s)
                count += 10
            print("=======================")
            if cl > 0: print(cl, "rows cleared!")
            print("Current score:", p)
            #reminder: 1 row cleared --> 40 points, 2 --> 100, 3 --> 300, 4 --> 1200
    return points

def fitness_function(board, strategy):
    game_scores = []
    count = 0
    for count in range(NUM_TRIALS): game_scores.append(play_game(board, strategy))
    for x in game_scores: count += x
    return count / len(game_scores)
def fitness_functionWithDisplay(board, strategy):
    game_scores = []
    points = 0
    for y in range(NUM_TRIALS): 
        p = play_gameWithDisplay(board, strategy, points)
        game_scores.append(p)
        points += p
    return points / len(game_scores)

HEIGHT = 20
NUM_VARIABLES = 6

def printboard(board):
    s = "=======================\n"
    for row in range(HEIGHT):
        s += ' '.join(list(("|" + board[row * 10: (row + 1) * 10] + "|"))) + " " + str(row) + "\n"
    s += "=======================\n\n"
    s += "  0 1 2 3 4 5 6 7 8 9  \n"
    return s

board = """
          
          
        # 
        ##
        ##
        ##
         #
        ##
         #
         #
        ##
        # 
        ##
        ##
        # 
   ###  ##
 ###### ##
    #### #
 ####### #
 ## ##### 
""".replace("\n", "")

board = """
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
##########
### ##### 
""".replace("\n", "")

play_game(board, tuple([random.uniform(-1, 1) for x in range(NUM_VARIABLES)]))