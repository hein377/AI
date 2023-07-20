import sys
N = int(sys.argv[1])
w = sys.argv[2]
ind1 = w.index("(")
ind2 = w.index(")")
w = w[ind1+1: ind2].split(", ")
W = tuple(int(x) for x in w)
B = float(sys.argv[3])
NUM_BITS = len(W)

def step(num):
    if(num > 0): return 1
    return 0

def dot_product(v1, v2):            #v1 and v2 are tuples; same size
    product, v1, v2 = 0, list(v1), list(v2)
    for i in range(NUM_BITS):
        product += v1[i] * v2[i]
    return product

def perceptron(A, w, b, x):         #returns f* = A(w dot x + b)
    return A(dot_product(w, x) + b)

def binary_to_decimal(binary):          #binary = string, decimal = int
    binaryls, decimal = list(binary), 0
    for i in range(length:=len(binaryls)):
        val = int(binaryls[i])
        decimal += val * (2**(length-1-i))
    return decimal

def decimal_to_binary(decimal, num_bits):
    binary = ""
    for i in range(num_bits-1, -1, -1):
        if(decimal - 2**i >= 0): 
            binary += "1"
            decimal -= 2**i
        else: binary += "0"
    return binary

def create_truth_table_in():            #returns [ (bits)<tuple_ints> ]; ie [ (1, 1), (1, 0) ... ] from largest to smallest
    global NUM_BITS
    binary_ins, num = [], 2**NUM_BITS - 1
    for i in range(num, -1, -1): binary_ins.append(tuple(int(n) for n in list(decimal_to_binary(i, NUM_BITS))))
    return binary_ins

TRUTH_TABLE_IN = create_truth_table_in()

def truth_table(bits, n):              #bits = #bits, n = canonical integer, returns { (inputs)<tuple_ints> : output<int> }
    truth_table, binary = {}, list(decimal_to_binary(n, 2**bits))
    for i in range(len(TRUTH_TABLE_IN)): truth_table.update({TRUTH_TABLE_IN[i] : int(binary[i])})
    return truth_table

def pretty_print_tt(table):
    for inputs, output in table.items():
        ls = list(inputs)
        for i in ls: print(i, end = "  ")
        print(f"|  {output}")

def check(n, w, b):                  #n = canonical integer, w = weight vector, b = bias scalar
    actual_table, result, count = truth_table(NUM_BITS, n), "", 0
    for x in TRUTH_TABLE_IN:         #x = input vector
        output = perceptron(step, w, b, x)
        if(output == actual_table[x]): count += 1
        result += str(output)
    trained_table = truth_table(NUM_BITS, binary_to_decimal(result))
    return count/len(TRUTH_TABLE_IN)

print(check(N, W, B))