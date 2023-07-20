from re import A
import numpy as np
import math
import sys 
import random

#GLOBAL VARIABLES
ARG = sys.argv[1]                   #argument for which challenge to run
NUM_EPOCHS = 500
LAMBDA = 10

#SETUP
def pretty_print_tt(table):
    for inputs, output in table.items():
        ls = list(inputs)
        for i in ls: print(i, end = "  ")
        print(f"|  {output}")

def sigmoid(dot):                       #input: np.array(); returnsa np.array() w/ sigmoid function applied to each entry
    arr = []
    for i in range(np.size(dot)): arr.append(1/(1+math.exp(-dot[0][i])))
    return np.array([arr])

def sigmoid_prime(dot):
    return sigmoid(dot) * (1-sigmoid(dot))

def find_dot(w, b, x): return (x@w) + b

def perceptron(A, dot): return A(dot)           #returns f* = A(w dot x + b)<np.array>

def calc_error(out, expected_out, length_of_arrays):                          #input: np.arrays(), same size
    return 1/length_of_arrays * (np.linalg.norm(expected_out - out))**2

def tuple_to_array(tup):
    ls = []
    for i in tup: ls.append(i)
    return np.array([ls])

def print_network(network):
    for l in range(len(network)):
        print(f"layer: {l}\nweight_matrix:\n{network[l][0]}\nbias_matrix:\n{network[l][1]}\n")

#BACKWARD PROPAGATION
def forward_propagate(x, network):                      #propagates through network and returns dot_vecs_ls and a_vecs_ls of; values of each layer
    a_vec = tuple_to_array(x)
    dot_vecs_ls, a_vecs_ls = [np.array([[0, 0]])], [a_vec]         #don't use dot_vec[0]; just a placeholder
    for layer in network:
        w_matrix, b_scalar = layer[0], layer[1]
        dot_vec = find_dot(w_matrix, b_scalar, a_vec)
        a_vec = perceptron(sigmoid, dot_vec)
        dot_vecs_ls.append(dot_vec)
        a_vecs_ls.append(a_vec)
    return a_vec, dot_vec, dot_vecs_ls, a_vecs_ls

def normal_back_propagation(actual_table, network):            #network = [ layer1, layer2, ... ]; layer1 = [ weight_matrix, bias_scalar ]              #actual_table = { (inputs)<tuple of floats> : (outputs)<tuple of floats> }   ie. {(1.0, 1.0): (0.0), (1.0, 0.0): (1.0), ... }
    #Training
    for i in range(NUM_EPOCHS):
        for x in actual_table.keys():
            #Forward Propagate
            a_vec, dot_vec, dot_vecs_ls, a_vecs_ls = forward_propagate(x, network)                            #a_vec = final hayer's output perceptron, dot_vec = final layer's dot
            #Backward Propagate - Calculate Gradient Descent Values
            delL_ls = [sigmoid_prime(dot_vec)*(tuple_to_array(actual_table[x])-a_vec)]                          #del_N           #del_Ls[-1] = delN (gradient function for LAST FUNCTION)
            for l in range(len(network)-2, -1, -1):
                delL_vector = sigmoid_prime(dot_vecs_ls[l+1]) * (delL_ls[0] @ (network[l+1][0]).T)
                delL_ls = [delL_vector] + delL_ls
            #Backward Propagate - Update Values
            for l in range(len(network)):
                layer = network[l]
                layer[1] = layer[1] + np.array([[LAMBDA]]) * delL_ls[l]                               #update bias
                layer[0] = layer[0] + np.array([[LAMBDA]]) * ((a_vecs_ls[l]).T @ delL_ls[l])              #update weight
    #Trained
    #Print final rounded perceptrons
'''    for x in actual_table.keys():
        a_vec = tuple_to_array(x)
        for layer in network:
                w_matrix, b_scalar = layer[0], layer[1]
                dot_vec = find_dot(w_matrix, b_scalar, a_vec)
                a_vec = perceptron(sigmoid, dot_vec)
        print(f"output perceptron: {np.rint(a_vec)}")'''

def back_propagationS(actual_table, network):            #network = [ layer1, layer2, ... ]; layer1 = [ weight_matrix, bias_scalar ]              #actual_table = { (inputs)<tuple of floats> : (outputs)<tuple of floats> }   ie. {(1.0, 1.0): (0.0), (1.0, 0.0): (1.0), ... }
    #Training
    for i in range(NUM_EPOCHS):
        for x in actual_table.keys():
            #Forward Propagate
            print(f"x: {x}")
            a_vec, dot_vec, dot_vecs_ls, a_vecs_ls = forward_propagate(x, network)                            #a_vec = final hayer's output perceptron, dot_vec = final layer's dot
            print(f"output_perceptron: {a_vec}")
            #Backward Propagate - Calculate Gradient Descent Values
            delL_ls = [sigmoid_prime(dot_vec)*(tuple_to_array(actual_table[x])-a_vec)]               #del_N           #del_Ls[-1] = delN (gradient function for LAST FUNCTION)
            for l in range(len(network)-2, -1, -1):
                delL_vector = sigmoid_prime(dot_vecs_ls[l+1]) * (delL_ls[0] @ (network[l+1][0]).T)
                delL_ls = [delL_vector] + delL_ls
            #Backward Propagate - Update Values
            for l in range(len(network)):
                layer = network[l]
                layer[1] = layer[1] + np.array([[LAMBDA]]) * delL_ls[l]                               #update bias
                layer[0] = layer[0] + np.array([[LAMBDA]]) * ((a_vecs_ls[l]).T @ delL_ls[l])              #update weight
            print()

def back_propagationC(actual_table, network):            #network = [ layer1, layer2, ... ]; layer1 = [ weight_matrix, bias_scalar ]              #actual_table = { (inputs)<tuple of floats> : (outputs)<tuple of floats> }   ie. {(1.0, 1.0): (0.0), (1.0, 0.0): (1.0), ... }
    #Training
    lamb = 0.1
    for i in range(300):
        for x in actual_table.keys():
            #Forward Propagate
            a_vec, dot_vec, dot_vecs_ls, a_vecs_ls = forward_propagate(x, network)                            #a_vec = final hayer's output perceptron, dot_vec = final layer's dot
            #Backward Propagate - Calculate Gradient Descent Values
            delL_ls = [sigmoid_prime(dot_vec)*(np.array([[actual_table[x]]])-a_vec)]               #del_N           #del_Ls[-1] = delN (gradient function for LAST FUNCTION)
            for l in range(len(network)-2, -1, -1):
                delL_vector = sigmoid_prime(dot_vecs_ls[l+1]) * (delL_ls[0] @ (network[l+1][0]).T)
                delL_ls = [delL_vector] + delL_ls
            #Backward Propagate - Update Values
            for l in range(len(network)):
                layer = network[l]
                layer[1] = layer[1] + np.array([[lamb]]) * delL_ls[l]                               #update bias
                layer[0] = layer[0] + np.array([[lamb]]) * ((a_vecs_ls[l]).T @ delL_ls[l])              #update weight
        lamb *= 0.99

        #Trained
        num_correct = 0
        for tup in actual_table.keys():
            x, y = tup
            a_vec = tuple_to_array(tup)
            for layer in network:
                w_matrix, b_scalar = layer[0], layer[1]
                dot_vec = find_dot(w_matrix, b_scalar, a_vec)
                a_vec = perceptron(sigmoid, dot_vec)
            if (x**2 + y **2 < 1) and (np.rint(a_vec) == 1): num_correct += 1
            elif (x**2 + y **2 > 1) and (np.rint(a_vec) == 0): num_correct += 1
        print(f"Epoch: {i}       Incorrect: {10000 - num_correct}")
    
def forward_propagate(x, network):                      #propagates through network and returns dot_vecs_ls and a_vecs_ls of; values of each layer
    a_vec = tuple_to_array(x)
    dot_vecs_ls, a_vecs_ls = [np.array([[0, 0]])], [a_vec]         #don't use dot_vec[0]; just a placeholder
    for layer in network:
        w_matrix, b_scalar = layer[0], layer[1]
        dot_vec = find_dot(w_matrix, b_scalar, a_vec)
        a_vec = perceptron(sigmoid, dot_vec)
        dot_vecs_ls.append(dot_vec)
        a_vecs_ls.append(a_vec)
    return a_vec, dot_vec, dot_vecs_ls, a_vecs_ls

#CHALLENGES
def create_random_wm(layer1_size, layer2_size):
    ls = []
    for row in range(layer1_size): ls.append([random.uniform(-1, 1) for i in range(layer2_size)])
    return np.array(ls)

def create_random_bs(layer_size): return np.array([[random.uniform(-1, 1) for i in range(layer_size)]])

#Challenge 1
w1, b1 = np.array([[1, -0.5], [1, 0.5]]), np.array([[1, -1]])
layer1 = [w1, b1]
w2, b2 = np.array([[1, 2], [-1, -2]]), np.array([[-0.5, 0.5]])
layer2 = [w2, b2]
network = [layer1, layer2]
x, y = np.array([[2, 3]]), np.array([[0.8, 1]])

normal_back_propagation({(2, 3) : (0.8, 1)}, network)

#Challenge 2: Train "SUM"
w1, b1 = create_random_wm(2, 2), create_random_bs(2)
w2, b2 = create_random_wm(2, 2), create_random_bs(2)
layer1 = [w1, b1]
layer2 = [w2, b2]
network = [layer1, layer2]
if(ARG == "S"): back_propagationS({(0, 0) : (0, 0), (0, 1) : (0, 1), (1, 0) : (0, 1), (1, 1) : (1, 0)}, network)

#Challenge 3: Train Circle
def create_training_set(filename):
    training_set = {}
    with open(filename) as f:
        for line in f:
            line = line.strip().split(" ")
            x, y = float(line[0]), float(line[1])
            if(x**2 + y **2 < 1): training_set.update({ (x, y) : (1) })
            else: training_set.update({ (x, y) : (0) })
    return training_set

expected_table = create_training_set("10000_pairs.txt")
w1, b1 = create_random_wm(2, 12), create_random_bs(12)
w2, b2 = create_random_wm(12, 4), create_random_bs(4)
w3, b3 = create_random_wm(4, 1), create_random_bs(1)
layer1, layer2, layer3 = [w1, b1], [w2, b2], [w3, b3]
network = [layer1, layer2, layer3]
if(ARG == "C"): back_propagationC(expected_table, network)
