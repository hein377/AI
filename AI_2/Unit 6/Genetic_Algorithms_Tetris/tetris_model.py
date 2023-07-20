import sys
import random
import math
import pickle

#Global Variables
HEIGHT = 20
WIDTH = 10
#board = sys.argv[1]              #len 200 string representation of tetrix_board
PIECES_INDS = { "I0":[0, 1, 2, 3], "I1":[0, -10, -20, -30], "O0":[0, 1, -10, -9], "T0":[0, -1, 1, -10], "T1":[0, -10, -9, -20], "T2":[0, -11, -10, -9], "T3":[0, -10, -11, -20], "S0":[0, 1, -9, -8], "S1":[0, -10, -11, -21], "Z0":[0, -1, -11, -12], "Z1":[0, -10, -9, -19], "J0":[0, 1, 2, -10], "J1":[0, -10, -20, -19], "J2":[0, -10, -11, -12], "J3":[0, -1, -10, -20], "L0":[0, -1, -2, -10], "L1":[0, 1, -10, -20], "L2":[0, -10, -9, -8], "L3":[0, -10, -20, -21] }           # { piecename<str> : [indices to add to get new indices to update]<list of ints> }
PIECE_LR_H = { "I0":(0, 3, 0), "I1":(0, 0, 3), "O0":(0, 1, 1), "T0":(-1, 1, 1), "T1":(0, 1, 2), "T2":(-1, 1, 1), "T3":(-1, 0, 2), "S0":(0, 2, 1), "S1":(-1, 0, 2), "Z0":(-2, 0, 0), "Z1":(0, 1, 2), "J0":(0, 2, 1), "J1":(0, 1, 2), "J2":(-2, 0, 1), "J3":(-1, 0, 2), "L0":(-2, 0, 1), "L1":(0, 1, 2), "L2":(0, 2, 1), "L3":(-1, 0, 2) }           # { piecename<str> : (left away from point, right away from point)<tuple of ints> }
PIECES = list(PIECES_INDS.keys())
rowcol_ind = {}                 # { (row, col)<tuple of ints> : ind<int> }
ind_rowcol = {}                 # { ind<int> : (row, col)<tuple of ints> }
#col_heights = {}                # { col<int> : colmaxrow<int> }
#boardmaxrow = 19

#Global Vars Set Up
def find_ind(row, col): return (row*WIDTH) + col
for row in range(HEIGHT):
    for col in range(WIDTH):
        rowcol_ind.update({ (row, col) : (ind:=find_ind(row, col)) })
        ind_rowcol.update({ ind : (row, col) })

def find_colheights_boardmaxrow(lsboard):
    global rowcol_ind
    col_heights, boardmaxrow = {}, 20
    for col in range(WIDTH):
        colheight = 20
        for row in range(HEIGHT-1, -1, -1):
            ind = rowcol_ind[(row, col)]
            if(lsboard[ind] == "#"): colheight = row
        col_heights.update({col : colheight})
        if(colheight < boardmaxrow): boardmaxrow = colheight
    return col_heights, boardmaxrow
    
#Part 1
def printboard(board):
    s = "=======================\n"
    for row in range(HEIGHT):
        s += ' '.join(list(("|" + board[row * 10: (row + 1) * 10] + "|"))) + " " + str(row) + "\n"
    s += "=======================\n\n"
    s += "  0 1 2 3 4 5 6 7 8 9  \n"
    return s

def make_row_blank(lsboard, row):
    for i in range(row * WIDTH, (row+1) * WIDTH):
        lsboard[i] = " "
    return lsboard

def replace_row(lsboard, row):                                             #replaces row with the row above
    for i in range(row*WIDTH, (row+1)*WIDTH): lsboard[i] = lsboard[i-WIDTH]
    return lsboard

def make_newboard(lsboard, row, maxrow):                                     #board<str>, row = completed_row<int>, max row <int>
    for r in range(row, maxrow, -1): lsboard = replace_row(lsboard, r)
    lsboard = make_row_blank(lsboard, maxrow)
    return lsboard

def num_rows_completed(board, bmaxrow, colhs):                                    #returns number of rows completed in input board and the updated board without completed rows, board<str>
    num, newboard = 0, list(board)
    for row in range(bmaxrow, HEIGHT):
        if(" " not in board[row*WIDTH:(row+1)*WIDTH]):                              #iterate thru board by row
            num += 1
            newboard = make_newboard(newboard, row, bmaxrow)                                 #delete completed row and shift rows above down by 1
            bmaxrow += 1
    return num, ''.join(newboard), find_colheights_boardmaxrow(newboard)

def place(lsboard, row, col, piece, boardmaxrow, col_heights):                                            #returns new board<string> with piece placed at specificed row and col
    global PIECES_INDS, rowcol_ind, ind_rowcol
    maxrow, colhs = boardmaxrow, col_heights.copy()
    testboard = lsboard.copy()
    i, inds_to_add = rowcol_ind[(row,col)], PIECES_INDS[piece]
    for ind in inds_to_add: 
        testboard[i+ind] = "#"
        new_r, new_c = ind_rowcol[i+ind]
        if new_r < boardmaxrow: maxrow = new_r
        colhs[new_c] = new_r
    return ''.join(testboard), maxrow, colhs

def out_of_bounds(i): return (i not in range(200))

def valid_ind(lsboard, row, col, piece):                                     #checks to see if the piece can be placed at the given row and col
    global PIECES_INDS, rowcol_ind
    i, inds_to_add = rowcol_ind[(row,col)], PIECES_INDS[piece]
    for ind in inds_to_add: 
        if(out_of_bounds(i+ind) or lsboard[i+ind] == "#"): return False
    return True

def pos_next_boards(lsboard, piece, boardmaxrow, col_heights):                                          #takes in current board and piece and returns every possible next board with the given piece placed
    global PIECE_LR_H
    ls = []
    left, right, h = PIECE_LR_H[piece]
    for col in range(0-left, WIDTH-right):
        candidate_row = col_heights[col]-1                  #first candidate row right above max row
        while(candidate_row >= 0 and (not valid_ind(lsboard, candidate_row, col, piece))): candidate_row -= 1
        if(candidate_row >= 0):
            placed_board, newboardmaxrow, new_colhs = place(lsboard, candidate_row, col, piece, boardmaxrow, col_heights)         #placed_board<str>
            rows_completed, completed_board, tup = num_rows_completed(placed_board, newboardmaxrow, new_colhs)          #completed_board<str>
            finalboardmaxrow, final_colhs = tup
            ls.append((completed_board, finalboardmaxrow, final_colhs, rows_completed))
        else:
            ls.append(("GAME OVER", None, None, 0))
    return ls                                               #ls = [ (completed_board<str>, board's_maxrow<int>, board's_col_heights<{int:int}>, num_rowscompleted<int>) OR ("GAME OVER", None, None, None), ... ]

#Part 2
def score(rows_completed):                                                       #cur_board <str>
    if(rows_completed == 0): return 0
    if(rows_completed == 1): return 40
    if(rows_completed == 2): return 100
    if(rows_completed == 3): return 300
    if(rows_completed == 4): return 1200
    return -math.inf

def newboard(): return [" "]*200

def select_randompiece(): return PIECES[random.randrange(0, len(PIECES))]

#Heuristic
def num_holes(board, c_h):
    global rowcol_ind
    holes = 0
    for col in c_h.keys():
        maxrow = c_h[col]
        for row in range(19, maxrow, -1):               #doesn't include maxrow
            if(board[rowcol_ind[(row,col)]] == " "): holes += 1
    return holes

def well_depth(board, c_h): return max(c_h.values())

def heights_sum(c_h): 
    s = 0
    for c in c_h: s += (HEIGHT-c_h[c])
    return s

def bumpiness(c_h): 
    b = 0
    for i in range(1, len(c_h)):
        cur_h, prev_h = c_h[i], c_h[i-1]
        b += abs((HEIGHT-cur_h) - (HEIGHT-prev_h))
    return b

def heuristic(tup, strategy):
    board, col_heights, maxrow, rows_completed = tup
    if(board == "GAME OVER"): return -10000
    #a, b, c, d, e, f = strategy
    a = strategy[0]
    value = 0
    value += a * rows_completed
    '''value += b * (20-maxrow)                                        #board's max height
    value += c * (nh:=num_holes(board, col_heights))
    value += d * (wd:=well_depth(board, col_heights))
    value += e * (hs:=heights_sum(col_heights))                     #each col's height summed
    value += f * (bp:=bumpiness(col_heights))'''
    return value

#Play Tetris
def best_board(pos_boards, strategy):
    if(len(pos_boards) == 0): return None, None, None, 0                 #no more possible moves --> game over
    max_heuristic_score = -math.inf
    best_tup = "", {}, 20, 0             #best_tup = bestboard, bestmaxrow, best_ch, best_rcompleted
    for tup in pos_boards:
        h_score = heuristic(tup, strategy)
        if(h_score == max_heuristic_score):
            if(random.uniform(0,1) <= 0.5): best_tup = tup
        elif(h_score > max_heuristic_score): 
            max_heuristic_score = h_score
            best_tup = tup
    bestboard, best_ch, bestmaxrow, best_rcompleted = best_tup
    return list(bestboard), best_ch, bestmaxrow, score(best_rcompleted)     #bestboard<list of str>

def play_game(strategy):                    #strategy is a set of numeric values (coefficients for heuristic)
    lsboard, points, score = newboard(), 0, 0
    col_heights, boardmaxrow = find_colheights_boardmaxrow(lsboard)
    while(lsboard != ['G', 'A', 'M', 'E', ' ', 'O', 'V', 'E', 'R']):
        piece = select_randompiece()
        pos_boards = pos_next_boards(lsboard, piece, boardmaxrow, col_heights)
        lsboard, col_heights, boardmaxrow, score = best_board(pos_boards, strategy)
        points += score
    return points

def play_game_w_print(strategy):                    #strategy is a set of numeric values (coefficients for heuristic)
    lsboard, points, score = newboard(), 0, 0
    col_heights, boardmaxrow = find_colheights_boardmaxrow(lsboard)
    print(printboard(''.join(lsboard)))
    print(f"Current score: {points}")
    while(lsboard != ['G', 'A', 'M', 'E', ' ', 'O', 'V', 'E', 'R']):
        piece = select_randompiece()
        pos_boards = pos_next_boards(lsboard, piece, boardmaxrow, col_heights)
        lsboard, col_heights, boardmaxrow, score = best_board(pos_boards, strategy)
        points += score
        if(lsboard == ['G', 'A', 'M', 'E', ' ', 'O', 'V', 'E', 'R']): 
            print("GAME OVER")
            print(f"Final score: {points}")
        else: 
            print(printboard(''.join(lsboard)))
            print(f"Current score: {points}", end = "\n\n")
    return points

#Neural Networks and back prop when there's r discrete categories you can classify; here the categories would be a continuum of how good a strategy is as opposed to discrete categories (ie types of stars)

#Global Variables
POPULATION_SIZE = 300
NUM_VARIABLES = 1                           #number of weights for strategy
NUM_CLONES = 25
NUM_TRIALS = 5
TOURNAMENT_SIZE = 30
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 2
MUTATION_RATE = .5

#POPULATION
def create_pop(popsize):                    #returns [ strategies ] where strategy = [a, b, c, d]
    strategies = []
    for i in range(popsize): strategies.append(tuple([random.uniform(-1, 1) for x in range(NUM_VARIABLES)]))
    return strategies

#FITNESS FUNCTION
def average(ls): return sum(ls)/len(ls)

def fitness_function(strategy):
    game_scores = []
    for i in range(NUM_TRIALS): 
        game_scores.append(play_game(strategy))
    return average(game_scores)

#SELECTION METHOD
def scorepop(pop):          #returns { strategy : score }, given pop = [ strategies ]
    dic, tot_score = {}, 0
    for i in range(len(pop)):
        strat = pop[i]
        score = fitness_function(strat)
        tot_score += score
        dic.update({strat:score})
        print(f"Evaluating strategy number {i} --> {score}")
    print(f"Average: {tot_score/POPULATION_SIZE}")
    return dic

def choose_parent(tournament):
    index = 0
    while(random.random() > TOURNAMENT_WIN_PROBABILITY): index += 1
    if(index >= len(tournament)): return tournament[len(tournament)-1]
    return tournament[index]

def create_tournaments(ranked_pop):
    randomindices, popsize = [] , len(ranked_pop)
    while(len(randomindices) < TOURNAMENT_SIZE*2):
        if (index:=random.randint(0, (popsize-1))) not in randomindices: randomindices.append(index)
    return sorted([randomindices[x] for x in range(TOURNAMENT_SIZE)]), sorted([randomindices[x] for x in range(TOURNAMENT_SIZE, TOURNAMENT_SIZE*2)])

#BREEDING
def create_child(parent1, parent2):                                     #parents are strategies <tuple of doubles>
    child = [None] * NUM_VARIABLES
    for i in range(CROSSOVER_LOCATIONS):                                #copy values at randominds from parent1
        random_ind = random.randint(0, NUM_VARIABLES-1)
        child[random_ind] = parent1[random_ind]
    for i in range(NUM_VARIABLES):                                         #copy remaining values from parent2
        if(child[i] == None): child[i] = parent2[i]
    return child                                                        #child = [ doubles ]

#MUTATION
def regenerate_val(child):                                              #child = [ doubles ]
    random_ind = random.randint(0, NUM_VARIABLES-1)
    child[random_ind] = random.uniform(-1, 1)
    return tuple(child)

def modify_val(child):                                                  #child = [ doubles ]
    random_ind = random.randint(0, NUM_VARIABLES-1)
    child[random_ind] *= 2
    return tuple(child)

def mutate(child):                                                      #child = [ doubles ]
    if(random.random() < MUTATION_RATE):
        if(random.uniform(0,1) <= 0.5): return regenerate_val(child)
        else: return modify_val(child)
    return tuple(child)

def create_nextgen(ranked_pop):
    nextgen = []
    for i in range(NUM_CLONES): nextgen.append(ranked_pop[i])        #CLONING
    while(len(nextgen) != len(ranked_pop)):
        tournament1, tournament2 = create_tournaments(ranked_pop)
        parent1, parent2 = ranked_pop[choose_parent(tournament1)], ranked_pop[choose_parent(tournament2)]
        child = mutate(create_child(list(parent1), list(parent2)))
        if(child not in nextgen): nextgen.append(child)
    return nextgen

#PROCESS
def process_pop(pop):
    scored_pop = scorepop(pop)                                                      #scored_pop = { strategy1<list of doubles> : fitness_function(strategy1)<double> ... }
    ranked_pop = sorted(pop, key = lambda x: scored_pop[x], reverse = True)         #ranked_pop = [ best_strategy, 2nd_best_strategy, ... ]
    return scored_pop, ranked_pop, ranked_pop[0]

def give_choices(scored_pop, generation, best_strategy):
    print(f"Generation: {generation}")
    print(f"Best strategy so far: {(best_strategy)} with score: {scored_pop[best_strategy]}")
    return input("(P)lay a game with current best strategy, (S)ave current process, or (C)ontinue? ")

def algo(tup, generation):
    scored_pop, ranked_pop, best_strat = tup
    c = give_choices(scored_pop, generation, best_strat)
    if(c == "C"): algo(process_pop(create_nextgen(ranked_pop)), generation+1)
    if(c == "P"): total_points = play_game_w_print(best_strat)
    if(c == "S"):
        filename = input("What filename? ")
        pickle.dump(scored_pop, open(filename, 'wb'))
        f = open("generation.txt", "w")
        f.write(str(generation))
        f.close()
        exit(0)

load = input("(N)ew process, or (L)oad saved process? ")
if(load == "N"):
    pop = create_pop(POPULATION_SIZE)
    algo(process_pop(pop), 0)

elif(load == "L"):
    filename = input("What filename? ")
    savefile = open(filename, 'rb')
    scored_pop = pickle.load(savefile)
    ranked_pop = sorted(scored_pop.keys(), key = lambda x: scored_pop[x], reverse = True)
    f = open("generation.txt", "r")
    algo((scored_pop, ranked_pop, ranked_pop[0]), int(f.readline()))
    
    
'''test = sys.argv[1].upper().replace("\n", " ")
count = 0
pop = create_pop(POPULATION_SIZE)
scoredic = scorepop(test, pop)
ranked_pop = sorted(pop, key = lambda x: scoredic[x], reverse = True)            #lambda x: scoredic[x] is equivalent to def func(x): return scoredic[x]; reverse = MAX to MIN instead of MIN to MAX
print(f"GENERATION: {count}     Score: {fitness_function(4, test, (best_cipher:=ranked_pop[0]))}")
print(decode(test, (best_cipher:=ranked_pop[0])))
count+=1
while(count < 100):
    pop = create_nextgen(pop, ranked_pop, scoredic, NUM_CLONES, TOURNAMENT_SIZE, TOURNAMENT_WIN_PROBABILITY, CROSSOVER_LOCATIONS, MUTATION_RATE) 
    scoredic = scorepop(test, pop)
    ranked_pop = sorted(pop, key = lambda x: scoredic[x], reverse = True)            #reverse = MAX to MIN instead of MIN to MAX
    print(f"GENERATION: {count}     Score: {fitness_function(4, test, (best_cipher:=ranked_pop[0]))}")
    print(decode(test, best_cipher))
    count += 1'''