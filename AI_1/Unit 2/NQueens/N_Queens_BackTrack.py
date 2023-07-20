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

def generate_board(size):
    return [-1 for i in range(size)]

def pass_vtest(state, row, col):
    return not col in state

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

def get_next_unassigned_var(state):     #row to try
    r = random.randint(0, size-1)
    while(state[r] != -1): 
        r = random.randint(0, size-1)
    return r

def get_sorted_values(state, row):      #possible columns to try
    pos_col = []
    for col in range(len(state)):
        if(pass_vtest(state, row, col) and pass_dtest(state, row, col)): pos_col.append(col)
    return pos_col

def csp_backtracking(state):        #state is a list
    if goal_test(state): return state
    row = get_next_unassigned_var(state)
    sorted_values = get_sorted_values(state, row)
    for i in range(length:=len(sorted_values)):
        col = sorted_values[random.randint(0, length-1)]
        new_state = state.copy() #create new_state by assigning val to var
        new_state[row] = col
        result = csp_backtracking(new_state)
        if result is not None:
            return result
    return None

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
for size in range(1, 45):
    start = time.perf_counter()
    print("Size: %s   Board: %s" % (size, state:=csp_backtracking(board(size))))
    end = time.perf_counter()
    if(not state is None): print(test_solution(state))
    print("Seconds to run: %s" % (end - start))
'''

#To Turn In:
start = time.perf_counter()
print("Size: %s   Board: %s" % (size:=33, state:=csp_backtracking(generate_board(size))))
print(test_solution(state))
print("Size: %s   Board: %s" % (size:=31, state:=csp_backtracking(generate_board(size))))
print(test_solution(state))
end = time.perf_counter()
print("Seconds to run: %s" % (end - start))