import random
import math
import numpy as np
import pickle

#Global Variables
IN_OUT_LS = []                          #[ ( input_array <1x784 np.array of ints>, output_array <1x10 np.array of ints> ), ... ]
NUM_EPOCHS = 65

#Set-up
def one_at_index(ind):
    ls = [0] * 10
    ls[int(ind)] = 1
    return ls

def div(ls, val): return [int(ls[i]) / val for i in range(len(ls))]

def process_data(filename):
    with open(filename) as f:
        for line in f:
            line = line.strip().split(",")
            input, output = np.array([div(line[1:], 255)]), np.array([one_at_index(line[0])])
            IN_OUT_LS.append((input, output))
process_data("mnist_train.csv")

def print_network(network):
    for l in range(len(network)):
        print(f"layer: {l}\nweight_matrix:\n{network[l][0]}\nbias_matrix:\n{network[l][1]}\n")

def create_random_wm(layer1_size, layer2_size):
    ls = []
    for row in range(layer1_size): ls.append([random.uniform(-1, 1) for i in range(layer2_size)])
    return np.array(ls)

def create_random_bs(layer_size): return np.array([[random.uniform(-1, 1) for i in range(layer_size)]])

def create_network(layer_sizes):        #layer_sizes = [input_layer_size, layer1_size, layer2_size,  ... ]
    network = []
    for i in range(1, len(layer_sizes)):
        size1 = layer_sizes[i-1]
        size2 = layer_sizes[i]                      #current layer size
        wm, bs = create_random_wm(size1, size2), create_random_bs(size2)
        network.append([wm, bs])
    return network

#BACKWARD PROPAGATION
def sigmoid(dot):                       #input: np.array(); returnsa np.array() w/ sigmoid function applied to each entry
    arr = []
    for i in range(dot.size): arr.append(1/(1+math.exp(-dot[0][i])))
    return np.array([arr])

def sigmoid_prime(dot):
    return (sig:=sigmoid(dot)) * (1-sig)

def find_dot(w, b, x): return (x@w) + b

def perceptron(A, dot): return A(dot)           #returns f* = A(w dot x + b)<np.array>

def forward_propagate(x, network):                      #propagates through network and returns dot_vecs_ls and a_vecs_ls of; values of each layer
    a_vec = x
    dot_vecs_ls, a_vecs_ls = [np.array([[0, 0]])], [a_vec]         #don't use dot_vec[0]; just a placeholder
    for layer in network:
        w_matrix, b_scalar = layer[0], layer[1]
        dot_vec = find_dot(w_matrix, b_scalar, a_vec)
        a_vec = perceptron(sigmoid, dot_vec)
        dot_vecs_ls.append(dot_vec)
        a_vecs_ls.append(a_vec)
    return a_vec, dot_vec, dot_vecs_ls, a_vecs_ls

def back_propagation(actual_table, network):            #network = [ layer1, layer2, ... ]; layer1 = [ weight_matrix, bias_scalar ]              #actual_table = [ ( input_array <1x784 np.array of ints>, output_array <1x10 np.array of ints> ), ... ]
    #Training
    lamb = 0.1
    for i in range(NUM_EPOCHS):
        count = 0
        for tup in actual_table:
            print(f"Epoch: {i}      tup: {count}")
            x, expected_output = tup
            #Forward Propagate
            a_vec, dot_vec, dot_vecs_ls, a_vecs_ls = forward_propagate(x, network)                            #a_vec = final layer's output perceptron, dot_vec = final layer's dot
            #Backward Propagate - Calculate Gradient Descent Values
            delL_ls = [sigmoid_prime(dot_vec)*(expected_output-a_vec)]                          #del_N           #del_Ls[-1] = delN (gradient function for LAST FUNCTION)
            for l in range(len(network)-2, -1, -1):
                delL_vector = sigmoid_prime(dot_vecs_ls[l+1]) * (delL_ls[0] @ (network[l+1][0]).T)
                delL_ls = [delL_vector] + delL_ls
            #Backward Propagate - Update Values
            for l in range(len(network)):
                layer = network[l]
                layer[1] = layer[1] + np.array([[lamb]]) * delL_ls[l]                               #update bias
                layer[0] = layer[0] + np.array([[lamb]]) * ((a_vecs_ls[l]).T @ delL_ls[l])              #update weight
            count += 1
        lamb *= 0.99
        pickle.dump(network, open('network.pkl', 'wb'))

#back_propagation(IN_OUT_LS, create_network([784, 300, 100, 10]))

savefile = open('network.pkl', 'rb')
network = pickle.load(savefile)
back_propagation(IN_OUT_LS, network)