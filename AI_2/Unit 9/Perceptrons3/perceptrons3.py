import sys
N = 2
in_vector = sys.argv[1]
in_vector = in_vector[in_vector.index("(")+1: in_vector.index(")")].split(", ")
IN_VECTOR = tuple(int(x) for x in in_vector)

def dot_product(v1, v2):                        #v1 and v2 are tuples; same size; returns scalar<int>
    product, v1, v2 = 0, list(v1), list(v2)
    for i in range(N):
        product += v1[i] * v2[i]
    return product

def step(num):
    if(num > 0): return 1
    return 0

def perceptron(A, w, b, x):         #returns f* = A(w dot x + b)
    return A(dot_product(w, x) + b)

def xor(x):                                     #x is a vector tuple
    w13, w23, b3 = 1, 1, 0
    w14, w24, b4 = -1, -2, 3
    w35, w45, b5 = 1, 2, -2
    p1 = perceptron(step, (w13, w23), b3, x)
    p2 = perceptron(step, (w14, w24), b4, x)
    p3 = perceptron(step, (w35, w45), b5, (p1, p2))         #XOR HAPPENS HERE
    return p3

print(xor(IN_VECTOR))