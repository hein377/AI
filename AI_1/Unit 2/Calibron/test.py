ex_height, ex_width = 10, 7
ex_area = ex_height * ex_width
board = ""
for i in range(ex_area):           #makes an empty board, a string w/ area number of dots, surrounded by !
    if(i < ex_width or (i >= ((ex_height * ex_width)-ex_width) and i < (ex_width * ex_height)) or i % ex_width == 0 or (i +1) % ex_width == 0): board += "!"
    else: board += "."

def printboard(board, h, w):
    for row in range(0, (w * (h-1))+1, w):
        for col in range(row, row+w):
            print(board[col], end = " ")
        print()

def put_block(board, blocknum, ind, dimensions):         #board is a list
    h, w = dimensions
    for row in range(ind, ind+1+((h-1)*ex_width), ex_width):
        for col in range(row, row+w):
            board[col] = str(blocknum)

printboard(board, ex_height, ex_width)
print()
lsboard = list(board)
put_block(lsboard, 7, 23, (3, 2))
printboard(''.join(lsboard), ex_height, ex_width)
put_block(lsboard, 4, 44, (2, 4))
printboard(''.join(lsboard), ex_height, ex_width)
result = [c for c in lsboard if c != "!"]
printboard(result, ex_height-2, ex_width-2)