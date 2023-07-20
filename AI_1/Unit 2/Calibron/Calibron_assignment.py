import sys

# You are given code to read in a puzzle from the command line.  The puzzle should be a single input argument IN QUOTES.
# A puzzle looks like this: "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4"
# The code below breaks it down:
puzzle = sys.argv[1].split()
puzzle_height = int(puzzle[0])
puzzle_width = int(puzzle[1])
rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
blocknum_dimensions = {}           #{symbol : set(dimension)}
area = 0
board = ""

#Setting up Global Variables
for i in range(len(rectangles)):
    x, y = rectangles[i]
    area += (x*y)
    if(i<=9): blocknum_dimensions.update({str(i) : {(x,y),(y,x)}})
    else: blocknum_dimensions.update({alphabet[i-9] : {(x,y),(y,x)}})

ex_width, ex_height = puzzle_width+2, puzzle_height+2
ex_area = ex_height * ex_width
for i in range(ex_area):           #makes an empty board, a string w/ area number of dots, surrounded by !
    if(i < ex_width or (i >= ((ex_height * ex_width)-ex_width) and i < (ex_width * ex_height)) or i % ex_width == 0 or (i +1) % ex_width == 0): board += "!"
    else: board += "."

def printboard(board, h, w):
    for row in range(0, (w * (h-1))+1, w):
        for col in range(row, row+w):
            print(board[col], end = " ")
        print()

# puzzle_height is the height (number of rows) of the puzzle
# puzzle_width is the width (number of columns) of the puzzle
# rectangles is a list of tuples of rectangle dimensions

# INSTRUCTIONS:
#
# First check to see if the sum of the areas of the little rectangles equals the big area.
# If not, output precisely this - "Containing rectangle incorrectly sized."
if((puzzle_height * puzzle_width) != area): print("Containing rectangle incorrectly sized.")

# Then try to solve the puzzle.
def goal_test(board):
    for blocknum in blocknum_dimensions.keys():
        if(blocknum not in board): return False
    return True

def get_next_unassigned_var(state):     #index to try (always top left corner)
    return state.index(".")

def fit_test(board, ind, dimensions):           #returns if dimensions fit and which dimensions fit (always in the form of height x width)
    h, w = dimensions
    for row in range(ind, ind+1+((h-1)*ex_width), ex_width):
        for col in range(row, row+w):
            if(board[col] != "."): return False
    return True

def get_sorted_values(board, ind):      #possible blocks to try at index
    pos_blocks = []                     #pos_blocks = [(block1, block1_dimensions)]
    for block, dimensions_set in blocknum_dimensions.items():
        for dimensions in dimensions_set:
            if(block not in board and fit_test(board, ind, dimensions)): pos_blocks.append((block, dimensions))
    return pos_blocks

def put_block(board, blocknum, ind, dimensions):         #board is a list
    h, w = dimensions
    for row in range(ind, ind+1+((h-1)*ex_width), ex_width):
        for col in range(row, row+w):
            board[col] = blocknum

def csp_backtracking(board):
    if goal_test(board): return board
    ind = get_next_unassigned_var(board)
    sorted_values = get_sorted_values(board, ind)
    for i in range(length:=len(sorted_values)):
        block, dimensions = sorted_values[i]
        new_board = list(board)
        put_block(new_board, block, ind, dimensions)
        result = csp_backtracking(''.join(new_board))
        if result is not None: return result
    return None

# If the puzzle is unsolvable, output precisely this - "No solution."
if((result:=csp_backtracking(board)) == None): print("No solution.")

# If the puzzle is solved, output ONE line for EACH rectangle in the following format:
# row column height width
# where "row" and "column" refer to the rectangle's top left corner.
#
# For example, a line that says:
# 3 4 2 1
# would be a rectangle whose top left corner is in row 3, column 4, with a height of 2 and a width of 1.
# Note that this is NOT the same as 3 4 1 2 would be.  The orientation of the rectangle is important.
result = [c for c in result if c != "!"]                #converts back to board w/o surrounding "!"s
def get_dimensions(blocknum, board, ind, dimensions_set):
    for dimensions in dimensions_set:
        height, width = dimensions
        wcount = 0
        while(ind < area and board[ind] == blocknum):
            wcount+=1
            ind+=1
        if(wcount == width): return height, width
        else: return width, height

for blocknum, dimensions_set in blocknum_dimensions.items():
    ind = result.index(blocknum)
    row, col = ind//puzzle_width, ind%puzzle_width
    h, w = get_dimensions(blocknum, result, ind, dimensions_set)
    print(f"{row} {col} {h} {w}")
# Your code should output exactly one line (one print statement) per rectangle and NOTHING ELSE.
# If you don't follow this convention exactly, my grader will fail.