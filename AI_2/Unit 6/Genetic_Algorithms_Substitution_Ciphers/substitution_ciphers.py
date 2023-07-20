from re import A
import sys
import random
from math import log

#Global Variables
source_alphabet = "ETAOINSHRDLCUMWFGYPBVKXJQZ"
ngram = {}                          #{ 4gram(str) : frequency(int) }

#Encoding and Decoding
def create_ciphera():
    return ''.join(random.sample(source_alphabet, len(source_alphabet)))

def encode(original, cipher_a):
    processed = ""
    for char in list(original):
        if(char in source_alphabet): processed += cipher_a[source_alphabet.index(char)]
        else: processed += char
    return processed

def decode(encoded, cipher_a):
    processed = ""
    for char in list(encoded):
        if(char in source_alphabet): processed += source_alphabet[cipher_a.index(char)]
        else: processed += char
    return processed

#Creating ngram dictionary
with open("ngrams.txt") as f:                   #store 4-grams frequencies
    for line in f:
        ls = line.strip().split(" ")
        if(len(ls[0]) == 4): ngram.update({ls[0] : int(ls[1])})

#Fitness Function
def containsonlyletters(strang):
    for i in range(len(strang)):
        if(strang[i] not in source_alphabet): return False
    return True

def process(word, n):
    ls = []
    for i in range(0, len(word)-(n-1)):
        if(containsonlyletters(w:=(word[i:i+n].upper())) and w in ngram.keys()): ls.append(word[i:i+n])
    return ls

def score(ls):
    total = 0
    for strang in ls: total += log(ngram[strang],2)
    return total

def fitness_function(n, encoded, cipher_a):
    decoded = decode(encoded, cipher_a)
    strings_to_score = process(decoded, n)              #List of n length strings from decoded string only containing letters
    return score(strings_to_score)

#Hill Climbing
def random_swap_ciphera(ciphera):
    ind1, ind2 = random.randint(0, len(ciphera)-1), random.randint(0, len(ciphera)-1)          #len(ciphera)-1 should always be 25 of course
    k = ciphera[ind1]
    ciphera[ind1] = ciphera[ind2]
    ciphera[ind2] = k
    return ciphera

def hill_climbing_loop(encoded, cipher, s):
    print(f"cipher: {cipher}, score: {s}")
    print(decode(encoded, cipher))
    input()
    swapped_cipher = random_swap_ciphera(cipher)
    if((score:=fitness_function(4, encoded, swapped_cipher)) > s): hill_climbing_loop(encoded, swapped_cipher, score)
    else: hill_climbing_loop(encoded, cipher, s)

def hill_climbing(encoded):
    candidate_ciphera = create_ciphera()
    score = fitness_function(4, encoded, candidate_ciphera)
    print(f"candidate cipher: {candidate_ciphera}, score: {score}")
    hill_climbing_loop(encoded, candidate_ciphera, score)

#Genetic Algorithm START

#Global Variables
POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = .8

#POPULATION
def create_pop(popsize):                    #popsize = POPULATION_SIZE
    pop = []
    while(len(pop) != popsize): 
        if((candidate_cipher:=create_ciphera()) not in pop): pop.append(candidate_cipher)
    return pop

#Already have FITNESS_FUNCTION()

#SELECTION METHOD
def scorepop(encoded, pop):          #returns { cipher : score } given pop = [ ciphers ]
    dic = {}
    for cipher in pop: dic.update({cipher:fitness_function(4, encoded, cipher)})
    return dic

def choose_parent(tournament, winprob):
    index = 0
    while(random.random() > winprob): index += 1
    if(index >= len(tournament)): return tournament[len(tournament)-1]
    return tournament[index]

def create_tournaments(ls, tourna_size):         #ls = list of sorted ciphers by score (greatest score to least), size = TOURNAMENT_SIZE
    randomindices, popsize = [] , len(ls)
    while(len(randomindices) < tourna_size*2):
        if (index:=random.randint(0, (popsize-1))) not in randomindices: randomindices.append(index)
    return sorted([randomindices[x] for x in range(tourna_size)]), sorted([randomindices[x] for x in range(tourna_size, tourna_size*2)])

#BREEDING
def create_child(parent1, parent2, num_swaps):
    child = [None] * 26
    for i in range(num_swaps):                                  #get num_swaps random indices and set element for child at those indices to the element for parent1 at those indices
        while(child[(random_ind:=random.randint(0, 25))] is not None):
            random_ind = random.randint(0, 25)
        child[random_ind] = parent1[random_ind]
    p_ind = 0
    for ind in range(len(child)):                               #Fill in child w/ unused chars from parent2
        if(child[ind] is None):
            while(parent2[p_ind] in child): p_ind += 1
            child[ind] = parent2[p_ind]
            p_ind += 1
        if(p_ind < len(parent2) and parent2[p_ind] in child): p_ind += 1
    return child

#MUTATION
def mutate(child, mutation_rate):
    if(random.random() < mutation_rate):
        return ''.join(random_swap_ciphera(child))
    return ''.join(child)

def create_nextgen(cur_gen, sortedlist, scoredic, numclones, tourn_size, tourn_winprob, num_swaps, mutation_rate):             #cur_gen = population, sortedlist = ranked_pop, numclones = NUM_CLONES, tourn_size = TOURNAMENT_SIZE, tourn_winprob = TOURNAMENT_WIN_PROBABILITY, num_swaps = CROSSOVER_LOCATIONS, mutation_rate = MUTATION_RATE
    nextgen = []
    for i in range(numclones): nextgen.append(sortedlist[i])        #CLONING
    while(len(nextgen) != len(cur_gen)):
        tournament1, tournament2 = create_tournaments(sortedlist, tourn_size)
        parent1, parent2 = sortedlist[choose_parent(tournament1, tourn_winprob)], sortedlist[choose_parent(tournament2, tourn_winprob)]           #strings
        child = mutate(create_child(list(parent1), list(parent2), num_swaps), mutation_rate)
        if(child not in cur_gen): nextgen.append(child)
    return nextgen

test = sys.argv[1].upper().replace("\n", " ")
count = 0
pop = create_pop(POPULATION_SIZE)
scoredic = scorepop(test, pop)
ranked_pop = sorted(pop, key = lambda x: scoredic[x], reverse = True)            #lambda x: scoredic[x] is equivalent to def func(x): return scoredic[x]; reverse = MAX to MIN instead of MIN to MAX
print(f"GENERATION: {count}     Score: {fitness_function(4, test, (best_cipher:=ranked_pop[0]))}")
print(decode(test, (best_cipher:=ranked_pop[0])))
count+=1
while(count < 100):
    pop = create_nextgen(pop, ranked_pop, scoredic, NUM_CLONES, TOURNAMENT_SIZE, TOURNAMENT_WIN_PROBABILITY, CROSSOVER_LOCATIONS, MUTATION_RATE) 
    scoredic = scorepop(test, pop)
    ranked_pop = sorted(pop, key = lambda x: scoredic[x], reverse = True)            #reverse = MAX to MIN instead of MIN to MAX
    print(f"GENERATION: {count}     Score: {fitness_function(4, test, (best_cipher:=ranked_pop[0]))}")
    print(decode(test, best_cipher))
    count += 1
