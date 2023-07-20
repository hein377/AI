import pickle

savefile = open('network.pkl', 'rb')
network = pickle.load(savefile)

def print_network(network):
    for l in range(len(network)):
        print(f"layer: {l}\nweight_matrix:\n{network[l][0]}\nbias_matrix:\n{network[l][1]}\n")

print_network(network)