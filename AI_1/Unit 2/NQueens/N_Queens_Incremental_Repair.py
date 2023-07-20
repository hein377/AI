import sys
import random
import time

def goal_test(state):
    if(-1 in state or not vg_test(state) or not dg_test(state)): return False
    return True

def vg_test(state):
    return len(state) == len(set(state))

def dg_test(state):
    for i in range(size):
        row, col = i, int(state[i])
        if(not pass_dtest(state, row, col)): return False
    return True

def generate_board(add_by):
    state, col = [], 0
    for row in range(size):
        state.append(col)
        col += add_by
        if(col >= size): col = (col+1)%size
    return state

def pass_vtest(state, row, col):
    for r in range(size):
        c = state[r]
        if(r != row and col == c): return False
    return True

def pass_dtest(state, row, col):
    return pass_dlutest(state, row, col) and pass_drutest(state, row, col) and pass_dldtest(state, row, col) and pass_drdtest(state, row, col)

def pass_dlutest(state, row, col):
    while(row > 0 and col > 0):
        row, col = row-1, col-1
        if(int(state[row]) == col): return False
    return True

def pass_drutest(state, row, col):
    while(row < size-1 and col > 0):
        row, col = row+1, col-1
        if(int(state[row]) == col): return False
    return True

def pass_dldtest(state, row, col):
    while(row > 0 and col < size-1):
        row, col = row-1, col+1
        if(int(state[row]) == col): return False
    return True

def pass_drdtest(state, row, col):
    while(row < size-1 and col < size-1):
        row, col = row+1, col+1
        if(int(state[row]) == col): return False
    return True

def printpuzzle(state):
    for row in range(size):
        for col in range(size):
            if(state[row] != col): print("x", end = '  ')
            else: print(str(col), end = '  ')
        print("\n")

def find_num_collisions(state):
    count = 0
    for row in range(size): count += num_attackers(state, row, state[row])
    return count//2

def solve(state):
    while(find_num_collisions(state) != 0):
        print("state: %s   num_collisions: %s" % (state, find_num_collisions(state)))
        marow = random.choice(most_attacked_queen_rows(state))
        state[marow] = random.choice(least_attacked_cols(state, marow))
    print("state: %s   num_collisions: %s" % (state, find_num_collisions(state)))        
    return state

def most_attacked_queen_rows(state):
    ls = []
    dic, max_attackers = row_attackers_dic(state)
    for row in range(size):
        if(dic[row] == max_attackers): ls.append(row)
    return ls

def row_attackers_dic(state):   # returns dic [row, #ofattackers]
    max_attackers = num_attackers(state, 0, state[0])
    dic = {0:max_attackers}
    for row in range(1, size):
        na = num_attackers(state, row, state[row])
        dic[row] = na
        if(na > max_attackers): max_attackers = na
    return dic, max_attackers

def least_attacked_cols(state, row):     
    ls = []
    dic, min_attackers = col_attackers_dic(state, row)
    for col in range(size):
        if(dic[col] == min_attackers): ls.append(col)
    return ls

def col_attackers_dic(state, row):      # return dic [col, #ofattackers]
    min_attackers = num_attackers(state, row, 0)
    dic = {0:min_attackers}
    for col in range(1, size):
        na = num_attackers(state, row, col)
        dic[col] = na
        if(na < min_attackers): min_attackers = na
    return dic, min_attackers

def random_pick(a, b):
    return random.choice([a,b])

def num_attackers(state, row, col):
    return v_attackers(state, row, col) + d_attackers(state, row, col)

def v_attackers(state, row, col):
    return up_attackers(state, row, col) + down_attackers(state, row, col)

def up_attackers(state, row, col):
    count = 0
    while row > 0:
        row -= 1
        c = state[row]
        if(col == c):
            count += 1
            break
    return count

def down_attackers(state, row, col):
    count = 0
    while row < size-1:
        row += 1
        c = state[row]
        if(col == c):
            count += 1
            break
    return count

def d_attackers(state, row, col):
    return dlu_attackers(state, row, col) + dru_attackers(state, row, col) + dld_attackers(state, row, col) + drd_attackers(state, row, col)

def dlu_attackers(state, row, col):
    count = 0
    while((row > 0 and col > 0)):
        row, col = row-1, col-1
        if(int(state[row]) == col): 
            count+=1
            break
    return count

def dru_attackers(state, row, col):
    count = 0
    while(row < size-1 and col > 0):
        row, col = row+1, col-1
        if(int(state[row]) == col): 
            count+=1
            break
    return count

def dld_attackers(state, row, col):
    count = 0
    while(row > 0 and col < size-1):
        row, col = row-1, col+1
        if(int(state[row]) == col): 
            count+=1
            break
    return count

def drd_attackers(state, row, col):
    count = 0
    while(row < size-1 and col < size-1):
        row, col = row+1, col+1
        if(int(state[row]) == col): 
            count+=1
            break
    return count

def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                print(var, "right", compare)
                return False
    return True

'''
for size in range(31,40):
    print("Size: %s" % size)
    start = time.perf_counter()
    solve(state:=generate_board(2))
    end = time.perf_counter()
    if(not state is None): print(test_solution(state))
    print("Seconds to run: %s" % (end - start))
    print("\n")
'''

start = time.perf_counter()
print("Size: %s   Board: %s" % (size:=32, state:=generate_board(2)))
print("Solved state: %s" % (solved:=solve(state)))
print(test_solution(solved))
print("Size: %s   Board: %s" % (size:=36, state:=generate_board(2)))
print("Solved state: %s" % (solved:=solve(state)))
print(test_solution(solved))
end = time.perf_counter()
print("Seconds to run: %s" % (end - start))