from functools import partial
from os import pathsep
import sys
#Global Varaibles
minlen = 0
dic = set()                                 #set of valid words
game = ""
winners = set()                             #winning letters
pos_next_games = {}                       #{game : set(possible_next_games)}
possibilities = set()

def game_over(game, cplayer):
    if(game in dic): return 1
    return None

def changeplayer(cplayer):
    if(cplayer == "cp"): return "p"
    if(cplayer == "p"): return "cp"

def negamax(game, cplayer):
    if((score:=game_over(game, cplayer)) != None): return score         #if the game is over, return the score based on the currentplayer determined by cplayersymbol
    results = []
    for next_game in pos_next_games[game]:                               #for the possible future boards (based cplayer's turn)
        results.append(-negamax(next_game, changeplayer(cplayer)))        #append the negative value of their return value since players are swapped and the value is based on player's turn
    return max(results)                                                         #always return the max of possible values since 1 means cp win and we assume perfect play by opponent

def getboardsfuture(game):             #{letter : (1, 0, or -1)}
    posnextgames, boardsfuture = pos_next_games[game], {}
    for next_game in posnextgames: boardsfuture.update({next_game[-1] : -negamax(next_game, "p")})
    return boardsfuture

#Set up Global Variables
def addtodic(dic, key, val):
    if key not in dic: dic.update({key : {val}})
    else: dic[key].add(val)

def process(dic, s, game):         #set of possible moves
    for word in s:
        partial_games = []
        for i in range((len(game)), len(word)+1): partial_games.append(word[:i])
        for i in range(len(partial_games)-1): addtodic(dic, partial_games[i], partial_games[i+1])

minlen = int(sys.argv[2])
if(len(sys.argv) > 3): game = sys.argv[3].lower()
with open("%s" % sys.argv[1]) as f:
    for line in f:
        if((l:=line.strip().lower()).isalpha() and (wordlen:=len(l)) >= minlen):                #> or >=
            if(l[:(gamelen:=len(game))] == game and wordlen > gamelen): 
                possibilities.add(l)
                addtodic(pos_next_games, game, game+l[gamelen])
            dic.add(l)

process(pos_next_games, possibilities, game)
boardsfuture = getboardsfuture(game)
for letter, result in boardsfuture.items():
    if(result == 1): winners.add(letter.upper())
if(len(winners) == 0): print("Next player will lose!")
else: print(winners)