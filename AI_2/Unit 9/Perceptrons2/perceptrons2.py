#Your goal is to write code that will determine how many n-bit Boolean functions can be 
#perfectly modeled by a perceptron, for (in theory) any value of n (though n > 4 is impractical).

import sys

#Global Variables
N = int(sys.argv[1])                   #number of bits, use n <= 4 for this assignment
NUM = int(sys.argv[2])                 #canonical integer output
NUM_EPOCHS = 100
LAMBDA1 = 1

#Generate every truth table
def binary_to_decimal(binary):                  #binary = string, decimal = int
    binaryls, decimal = list(binary), 0
    for i in range(length:=len(binaryls)):
        val = int(binaryls[i])
        decimal += val * (2**(length-1-i))
    return decimal

def decimal_to_binary(decimal, num_bits):       #binary = string, decimal = int
    binary = ""
    for i in range(num_bits-1, -1, -1):
        if(decimal - 2**i >= 0): 
            binary += "1"
            decimal -= 2**i
        else: binary += "0"
    return binary

def create_truth_table_in():            #returns [ (bits)<tuple_ints> ]; ie [ (1, 1), (1, 0) ... ] from largest to smallest
    global N
    binary_ins, num = [], 2**N - 1
    for i in range(num, -1, -1): binary_ins.append(tuple(int(n) for n in list(decimal_to_binary(i, N))))
    return binary_ins

def truth_table(bits, num):              #bits = #bits, num = canonical integer, returns { (inputs)<tuple_ints> : output<int> }
    truth_table, binary = {}, list(decimal_to_binary(num, 2**bits))
    for i in range(len(TRUTH_TABLE_IN)): truth_table.update({TRUTH_TABLE_IN[i] : int(binary[i])})
    return truth_table

def pretty_print_tt(table):
    for inputs, output in table.items():
        ls = list(inputs)
        for i in ls: print(i, end = "  ")
        print(f"|  {output}")

TRUTH_TABLE_IN = create_truth_table_in()            #[ (1, 1), (1, 0) ... ]

#Train Perceptron
def step(num):
    if(num > 0): return 1
    return 0

def dot_product(v1, v2):                        #v1 and v2 are tuples; same size; returns scalar<int>
    product, v1, v2 = 0, list(v1), list(v2)
    for i in range(N):
        product += v1[i] * v2[i]
    return product

def scalar_times_vector(s, v):        #scalar s <int>, vector v <tuple_ints>; returns vector<tuple_ints>
    ls = list(v)
    for i in range(len(ls)): ls[i] *= s
    return tuple(ls)

def vector_plus_vector(v1, v2):       #vector v1 <tuple_ints>, vector v2 <tuple_ints>, returns vector<tuple_ints>
    addedls, vec1, vec2 = [], list(v1), list(v2)
    for i in range(len(v1)): addedls.append(vec1[i] + vec2[i])
    return tuple(addedls)

def perceptron(A, w, b, x):         #returns f* = A(w dot x + b)
    return A(dot_product(w, x) + b)

def create_table(w, b):
    trained_table = {}
    for x in TRUTH_TABLE_IN: trained_table.update({ x : perceptron(step, w, b, x) })
    return trained_table

def train_perceptron(actual_table):                  #actual_table = { (inputs)<tuple_ints> : output<int> }   ie. {(1, 1): 0, (1, 0): 1, (0, 1): 0, (0, 0): 1}
    global N
    w, b = tuple(0 for i in range(N)), 0
    last_epoch = [w, b]                     #epochs = [ (vector_w), scalar_b ]
    print(actual_table)
    for i in range(NUM_EPOCHS):
        for x in TRUTH_TABLE_IN:
            f = perceptron(step, w, b, x)
            w = vector_plus_vector(w, scalar_times_vector((actual_table[x] - f) * LAMBDA1, x))
            b = b + (actual_table[x] - f)
        if (ls:=[w, b]) == last_epoch: return create_table(w, b), w, b
        else: last_epoch = ls
    return None, None, None

def check(num):                  #num = canonical integer, w = weight vector, b = bias scalar
    actual_table, count = truth_table(N, num), 0
    trained_table, w, b = train_perceptron(actual_table)
    if(trained_table == None): return 0
    for x in TRUTH_TABLE_IN:
        if(actual_table[x] == trained_table[x]): count += 1
    return w, b, count/len(TRUTH_TABLE_IN)

def process():
    global N
    max_num, correct = 2**(2**N) - 1, 0
    for num in range(max_num, -1, -1):
        w, b, percent = check(num)
        if percent == 1.0: correct += 1
    print(f"{max_num+1} possible functions; {correct} can be correctly modeled.")

w, b, percent = check(NUM)
print(f"weight_vector: {w}")
print(f"bias_value: {b}")
print(f"percent: {percent}")

'''
2. Generate every truth table possible with that number of bits (ie, loop over each possible value for canonical
integer representation for that number of bits, returning the truth table for each one.)
3. For each truth table:
a. Start a perceptron model with a zero vector for weight and a zero value for bias and run the perceptron
training algorithm until it completes, as shown in the video.
b. TEST THE ACCURACY of the completed perceptron by looping over the truth table one more time and
calculating the percentage of input vectors that are categorized correctly by your final perceptron.
4. Output the total number of possible functions, and how many of those truth tables could be 100% correctly
modeled. For example, for n = 2, the answer should be “16 possible functions; 14 can be correctly modeled.”
'''
