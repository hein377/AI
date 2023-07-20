import random
import sys
from math import log
source_alphabet = "ETAOINSHRDLCUMWFGYPBVKXJQZ"
ngram = {}                          #{ 4gram(str) : frequency(int) }

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

def random_swap_ciphera(ciphera):                   #chooses 2 random indices, swaps elements at those 2 indices in the cipher, return the cipher
    ind1, ind2 = random.randint(0, len(ciphera)-1), random.randint(0, len(ciphera)-1)
    k = ciphera[ind1]
    ciphera[ind1] = ciphera[ind2]
    ciphera[ind2] = k
    return ciphera

#Creating ngram dictionary
with open("ngrams.txt") as f:                   #store 4-grams frequencies
    for line in f:
        ls = line.strip().split(" ")
        if(len(ls[0]) == 4): 
            ngram.update({ls[0] : int(ls[1])})

#START OF GENETIC ALGO
#Global Variables
POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = .8

#POPULATION
def create_pop(popsize):                    #Creates generation 0 with random ciphers
    pop = []
    while(len(pop) != popsize):
        if((candidate_cipher:=create_ciphera()) not in pop): pop.append(candidate_cipher)
    return pop

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

def score(ls):                  #Takes in list of strings only containing letters from decoded message and check if each of them are in the n gram dictionary and add its score to total if it is
    total = 0
    for strang in ls: total += log(ngram[strang],2)
    return total

def fitness_function(n, encoded, cipher_a):
    decoded = decode(encoded, cipher_a)
    strings_to_score = process(decoded, n)              #List of n length strings from decoded string only containing letters
    return score(strings_to_score)

#SELECTION METHOD
def scorepop(encoded, pop):          #returns { cipher : score } given pop = [ ciphers ]
    dic = {}
    for cipher in pop: dic.update({cipher:fitness_function(4, encoded, cipher)})
    return dic

def choose_parent(tournament, winprob):
    index = 0
    while(random.random() > winprob): index += 1
    if(index >= len(tournament)): return tournament[len(tournament)-1]          #If random.random has repeatedly chosen numbers > winprob so much so that index is now out of bounds, choose the last element in the tournament
    return tournament[index]

def create_tournaments(ls, tourna_size):         #ls = list of sorted ciphers by score (greatest score to least), size = TOURNAMENT_SIZE
    randomindices, popsize = [] , len(ls)
    while(len(randomindices) < tourna_size*2):
        if (index:=random.randint(0, (popsize-1))) not in randomindices: randomindices.append(index)                                                #creates list of random indices without repeats
    return sorted([randomindices[x] for x in range(tourna_size)]), sorted([randomindices[x] for x in range(tourna_size, tourna_size*2)])            #forms sorted tournament1 from first half of list and sorted tournament 2 from second half of list

#BREEDING
def create_child(parent1, parent2, num_swaps):
    child = [None] * 26
    for i in range(num_swaps):                                  #get num_swaps random indices and set element for child at those indices to the element from parent1 at those indices
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

def create_nextgen(cur_gen, sortedlist, numclones, tourn_size, tourn_winprob, num_swaps, mutation_rate):             #cur_gen = population, sortedlist = ranked_pop, numclones = NUM_CLONES, tourn_size = TOURNAMENT_SIZE, tourn_winprob = TOURNAMENT_WIN_PROBABILITY, num_swaps = CROSSOVER_LOCATIONS, mutation_rate = MUTATION_RATE
    nextgen = []
    for i in range(numclones): nextgen.append(sortedlist[i])        #CLONING
    while(len(nextgen) != len(cur_gen)):
        tournament1, tournament2 = create_tournaments(sortedlist, tourn_size)
        parent1, parent2 = pop[choose_parent(tournament1, tourn_winprob)], pop[choose_parent(tournament2, tourn_winprob)]
        child = mutate(create_child(list(parent1), list(parent2), num_swaps), mutation_rate)
        if(child not in cur_gen): nextgen.append(child)
    return nextgen    

tests = ["""
PF Hacyhttrq vf n pbyyrpgvba bs serr yrneavat npgvivgvrf gung grnpu Pbzchgre Fpvrapr guebhtu ratntvat tnzrf naq chmmyrf gung hfr pneqf, fgevat, penlbaf naq ybgf bs ehaavat nebhaq. Jr bevtvanyyl qrirybcrq guvf fb gung lbhat fghqragf pbhyq qvir urnq-svefg vagb Pbzchgre Fpvrapr, rkcrevrapvat gur xvaqf bs dhrfgvbaf naq punyyratrf gung pbzchgre fpvragvfgf rkcrevrapr, ohg jvgubhg univat gb yrnea cebtenzzvat svefg.

Gur pbyyrpgvba jnf bevtvanyyl vagraqrq nf n erfbhepr sbe bhgernpu naq rkgrafvba, ohg jvgu gur nqbcgvba bs pbzchgvat naq pbzchgngvbany guvaxvat vagb znal pynffebbzf nebhaq gur jbeyq, vg vf abj jvqryl hfrq sbe grnpuvat. Gur zngrevny unf orra hfrq va znal pbagrkgf bhgfvqr gur pynffebbz nf jryy, vapyhqvat fpvrapr fubjf, gnyxf sbe fravbe pvgvmraf, naq fcrpvny riragf.

Gunaxf gb trarebhf fcbafbefuvcf jr unir orra noyr gb perngr nffbpvngrq erfbheprf fhpu nf gur ivqrbf, juvpu ner vagraqrq gb uryc grnpuref frr ubj gur npgvivgvrf jbex (cyrnfr qba’g fubj gurz gb lbhe pynffrf – yrg gurz rkcrevrapr gur npgvivgvrf gurzfryirf!). Nyy bs gur npgvivgvrf gung jr cebivqr ner bcra fbhepr – gurl ner eryrnfrq haqre n Perngvir Pbzzbaf Nggevohgvba-FunerNyvxr yvprapr, fb lbh pna pbcl, funer naq zbqvsl gur zngrevny.

Sbe na rkcynangvba ba gur pbaarpgvbaf orgjrra PF Hacyhttrq naq Pbzchgngvbany Guvaxvat fxvyyf, frr bhe Pbzchgngvbany Guvaxvat naq PF Hacyhttrq cntr.

Gb ivrj gur grnz bs pbagevohgbef jub jbex ba guvf cebwrpg, frr bhe crbcyr cntr.

Sbe qrgnvyf ba ubj gb pbagnpg hf, frr bhe pbagnpg hf cntr.

Sbe zber vasbezngvba nobhg gur cevapvcyrf oruvaq PF Hacyhttrq, frr bhe cevapvcyrf cntr.""".upper().replace("\n", " ")]

for test in tests:
    #Creates Generation 0 and tests it out
    count = 0
    pop = create_pop(POPULATION_SIZE)
    scoredic = scorepop(test, pop)              #Creates dictionary { ciphers(str) : scores(double) }
    ranked_pop = sorted(pop, key = lambda x: scoredic[x], reverse = True)            #sorts the scored ciphers dictionary
    print(f"GENERATION: {count}     Score: {fitness_function(4, test, (best_cipher:=ranked_pop[0]))}")
    print(decode(test, (best_cipher:=ranked_pop[0])))
    count+=1
    while(count < 1000):
        pop = create_nextgen(pop, ranked_pop, NUM_CLONES, TOURNAMENT_SIZE, TOURNAMENT_WIN_PROBABILITY, CROSSOVER_LOCATIONS, MUTATION_RATE) 
        scoredic = scorepop(test, pop)
        ranked_pop = sorted(pop, key = lambda x: scoredic[x], reverse = True)            #reverse = MAX to MIN instead of MIN to MAX
        print(f"GENERATION: {count}     Score: {fitness_function(4, test, (best_cipher:=ranked_pop[0]))}")
        print(decode(test, best_cipher))
        input()
        count += 1