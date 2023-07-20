import sys

#Writing DFAs
dfa1 = {
    0: {
        "a": 1
    },
    1: {
        "a": 2
    },
    2: {
        "b": 3
    },
    3: {}
}
final1 = [3]
chars1 = ["a", "b"]

dfa2 = {
    0: {
        "0": 0,
        "2": 0,
        "1": 1
    },
    1: {
        "0": 0,
        "2": 0,
        "1": 1
    }
}
final2 = [1]
chars2 = ["0", "1", "2"]

dfa3 = {
    0: {
        "a": 0,
        "c": 0,
        "b": 1
    },
    1: {
        "a": 1,
        "b": 1,
        "c": 1
    }
}
final3 = [1]
chars3 = ["a", "b", "c"]

dfa4 = {
    0: {
        "1": 0,
        "0": 1
    },
    1: {
        "1": 1,
        "0": 0
    }
}
final4 = [0]
chars4 = ["0", "1"]

dfa5 = {
    0: {
        "0": 2,
        "1": 1
    },
    1: {
        "0": 3,
        "1": 0
    },
    2: {
        "0": 0,
        "1": 3
    },
    3: {
        "0": 1,
        "1": 2
    }
}
final5 = [0]
chars5 = ["0", "1"]

dfa6 = {
    0: {
        "a": 1,
        "b": 0,
        "c": 0
    },
    1: {
        "a": 1,
        "b": 2,
        "c": 0
    },
    2: {
        "a": 1,
        "b": 0,
        "c": 3
    },
    3: {}
}
final6 = [0,1,2]
chars6 = ["a", "b", "c"]

dfa7 = {
    0: {
        "0": 1,
        "1": 0,
    },
    1: {
        "0": 1,
        "1": 2,
    },
    2: {
        "0": 2,
        "1": 3,
    },
    3: {
        "0": 2,
        "1": 4,
    },
    4: {
        "0": 4,
        "1": 4,
    }
}
final7 = [4]
chars7 = ["0", "1"]

#Global Variables
chars = []                  #available characters in DFA
final_states = []           #indices of final states of DFA
dfa = {}                  #{ initial_state_ind(int) : {char(str) : final_state_ind(int)} }

#Setting up dfa dictionary
if("txt" in sys.argv[1]):
    ls = open(f"{sys.argv[1]}", "r").read().splitlines()
    chars = [c for c in list(ls[0])]
    final_states = [int(state) for state in ls[2].split(' ')]

    state = -999
    for i in range(4,len(ls)):
        x = ls[i]
        if(len(x) == 1): 
            state = int(x)
            dfa.update({state:dict()})
        elif(len(x) != 0):
            l = x.split()
            dfa[state].update({l[0]:int(l[1])})

else: exec(fr"dfa, chars, final_states = dfa{sys.argv[1]}, chars{sys.argv[1]}, final{sys.argv[1]}")

#Print the transition info table
def printtable(chars, dfa):
    print("*", end = '')
    for char in chars: print(f"     {char}", end = '')
    print()
    for i in dfa.keys():
        print(str(i), end = '')
        for char in chars: 
            if(char in dfa[i].keys()): print(f"     {dfa[i][char]}", end = "")
            else: print(f"     _", end = "")
        print()
printtable(chars, dfa)

#Running dfa on test cases in textfile
def dfa_process(strang):
    curstate, dic = 0, dfa[0]
    for i in range(len(strang)):
        if(((char:=strang[i]) not in chars) or (char not in dic.keys())): return False
        else: curstate, dic = dic[char], dfa[dic[char]]
    return (curstate in final_states)

with open(f"{sys.argv[2]}") as f:
    for line in f:
        test = line.strip()
        if(dfa_process(test)): print(f"True  {test}")
        else: print(f"False {test}")