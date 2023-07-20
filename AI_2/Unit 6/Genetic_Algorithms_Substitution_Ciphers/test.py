import random
source_alphabet = "ETAOINSHRDLCUMWFGYPBVKXJQZ"
ngram = {}                          #{ 4gram(str) : frequency(int) }

#Encoding and Decoding
def create_tournaments(tourna_size):         #ls = list of sorted ciphers by score (greatest score to least), size = TOURNAMENT_SIZE
    randomindices, popsize = [] , 500
    while(len(randomindices) < tourna_size*2):
        if (index:=random.randint(0, (popsize-1))) not in randomindices: randomindices.append(index)
    print(f"random_indices{randomindices}")
    return sorted([randomindices[x] for x in range(tourna_size)]), sorted([randomindices[x] for x in range(tourna_size, tourna_size*2)])

def choose_parent(tournament, winprob):
    index = 0
    while(random.random() > winprob): index += 1
    if(index >= len(tournament)): return tournament[len(tournament)-1]
    return tournament[index]

def create_child(parent1, parent2, num_swaps):
    child = [None] * 5
    for i in range(num_swaps):                                  #get num_swaps random indices and set element for child at those indices to the element for parent1 at those indices
        while(child[(random_ind:=random.randint(0, 4))] is not None):
            random_ind = random.randint(0, 4)
        child[random_ind] = parent1[random_ind]
    print(child)
    input()
    p_ind = 0
    for ind in range(len(child)):                               #Fill in child w/ unused chars from parent2
        if(child[ind] is None):
            while(parent2[p_ind] in child): p_ind += 1
            child[ind] = parent2[p_ind]
            p_ind += 1
        if(p_ind < len(parent2) and parent2[p_ind] in child): p_ind += 1
    print(child)
    input()
    return child

tournament1, tournament2 = create_tournaments(5)
print(f"tournament1: {tournament1}, tournament2: {tournament2}")
print(f"parent1: {choose_parent(tournament1, .75)}")
print(f"parent2: {choose_parent(tournament2, .75)}")
print()
print(create_child("ABCDE", "EBCDA", 2))