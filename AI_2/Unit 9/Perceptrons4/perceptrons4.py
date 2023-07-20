import sys
import numpy as np
import math
import random

def step(num): return 1 if(num > 0) else 0                  #input: num<np.array> of size 1x1; returns 0 or 1<int>
def sigmoid(num): return 1/(1+math.exp(-num))

def perceptron(A, w, b, x): return A(w@(x.T) + b)           #returns f* = A(w dot x + b)<int>

def xor(x):                                                 #x is a np array
    w3, b3 = np.array([[1, 1]]), np.array([[0]])
    w4, b4 = np.array([[-1, -2]]), np.array([[3]])
    w5, b5 = np.array([[1, 2]]), np.array([[-2]])                 #2-bit input AND
    p1 = perceptron(step, w3, b3, x)
    p2 = perceptron(step, w4, b4, x)
    return perceptron(step, w5, b5, np.array([[p1, p2]]))         #XOR HAPPENS HERE

def diamond(x):                                              #x is a np array
    w1, b1 = np.array([[1.0, -1.0]]), np.array([[1.0]])
    w2, b2 = np.array([[-1.0, 1.0]]), np.array([[1.0]])
    w3, b3 = np.array([[-1.0, -1.0]]), np.array([[1.0]])
    w4, b4 = np.array([[1.0, 1.0]]), np.array([[1.0]])
    #w5, b5 = np.array([[1, 2, 3, 4]]), np.array([[-9]])                 #4-bit input AND
    w5, b5 = np.array([[1.0, 1.0, 1.0, 1.0]]), np.array([[-3.99]])
    p1 = perceptron(step, w1, b1, x)
    p2 = perceptron(step, w2, b2, x)
    p3 = perceptron(step, w3, b3, x)
    p4 = perceptron(step, w4, b4, x)
    return perceptron(step, w5, b5, np.array([[p1, p2, p3, p4]]))

def circle(x):                                              #x is a np array
    i, j = 0.1, -3.99
    w1, b1 = np.array([[1, -1]]), np.array([[i]])
    w2, b2 = np.array([[-1, 1]]), np.array([[i]])
    w3, b3 = np.array([[-1, -1]]), np.array([[i]])
    w4, b4 = np.array([[1, 1]]), np.array([[i]])
    w5, b5 = np.array([[1, 1, 1, 1]]), np.array([[j]])              #4-bit input AND
    p1 = perceptron(sigmoid, w1, b1, x)
    p2 = perceptron(sigmoid, w2, b2, x)
    p3 = perceptron(sigmoid, w3, b3, x)
    p4 = perceptron(sigmoid, w4, b4, x)
    return round(perceptron(sigmoid, w5, b5, np.array([[p1, p2, p3, p4]])))

def generatexy(n): return [np.array([[random.uniform(-1, 1), (random.uniform(-1, 1))]]) for i in range(n)]

def test_circle(invector_ls):
    correct = 0
    for in_vector in invector_ls:
        x, y = in_vector[0][0], in_vector[0][1]
        expected_val, output_val = 0, circle(in_vector)
        if(x**2 + y **2 < 1): epected_val = 1
        if(expected_val == output_val): correct += 1
    return correct / len(invector_ls)

'''#Finding good i-value (i = 0.1 in this case)
i_dic = dict()                          #{ i_val : %_accuracy }
for i in range(0, 20):
    i_dic.update({ (i/10) : test_circle(invector_ls, i/10, -3.99)})
print(i_dic)'''

args = sys.argv
if(len(args)==2):
    in_vector = args[1]
    in_vector = in_vector[in_vector.index("(")+1: in_vector.index(")")].split(", ")
    in_vector = np.array([list(float(x) for x in in_vector)])
    print(xor(in_vector))
elif(len(args) == 3):
    x, y = args[1], args[2]                 #decimal values
    output = diamond(np.array([[float(x), float(y)]]))
    if(output == 1): print("inside")
    else: print("outside")
elif(len(args) == 1):
    invector_ls = generatexy(500)
    print(test_circle(invector_ls))

'''
1. If you receive one command-line input, then it will be a string of a tuple containing a pair of Boolean inputs, for
example “(1, 0)”. In this case, run those inputs through your XOR network and print out the result. (Make sure
you’ve commented “XOR HAPPENS HERE” again so I can see you’re using matrices now!) This is how I will check
challenge 1.
2. If you receive two command-line inputs, then each one will be a decimal value. Use the first as x and the second
as y, and output “inside” or “outside” based on your step-function diamond code (not the circle challenge). This
is how I will check challenge 2.
3. If you receive zero command-line inputs, then generate 500 random points as described in the circle challenge.
Run them all through your hardcoded best results sigmoid circle network. Output the coordinates of any
misclassified points, and print the percentage of the 500 that were classified correctly. This is how I will check
challenge 3.
'''