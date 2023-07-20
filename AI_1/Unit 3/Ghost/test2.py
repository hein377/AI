from os import pathsep
import sys

#Global Varaibles
minlen = 0
dic = set()                                 #set of valid words
game = ""
winners = set()                             #winning letters
possibilities = set()
pos_next_games = {}

def game_over(game, cplayer):
    if(game in dic): return 1
    return None

def changeplayer(cplayer):
    if(cplayer == "cp"): return "p"
    if(cplayer == "p"): return "cp"

def possible_next_games(game):
    pos_next_games = set()
    for word in possibilities: 
        if(len(word) > (gamelen:=len(game)) and word[:gamelen] == game): pos_next_games.add(game+word[gamelen])
    return pos_next_games

def negamax(game, cplayer):
    if((score:=game_over(game, cplayer)) != None): return score         #if the game is over, return the score based on the currentplayer determined by cplayersymbol
    results = []
    for next_game in possible_next_games(game):                               #for the possible future boards (based cplayer's turn)
        results.append(-negamax(next_game, changeplayer(cplayer)))        #append the negative value of their return value since players are swapped and the value is based on player's turn
    return max(results)                                                         #always return the max of possible values since 1 means cp win and we assume perfect play by opponent

def getboardsfuture(game):             #{letter : (1, 0, or -1)}
    posnextgames, boardsfuture = possible_next_games(game), {}
    for next_game in posnextgames: boardsfuture.update({next_game[-1] : -negamax(next_game, "p")})
    return boardsfuture

#Set up Global Variables
def addtodic(dic, key, val):
    if key not in dic: dic.update({key : {val}})
    else: dic[key].add(val)

def process(s, dic, game):
    for word in s:
        if(len(word) > (gamelen:=len(game)) and word[:gamelen] == game): addtodic(dic, game, game+word[gamelen])
        
def getchildren(parent):
    while(len(parent) != 0):
        child = parent.pop()
        process(possibilities, pos_next_games, child)
        if(child not in dic): parent.update(pos_next_games[child])

minlen = int(sys.argv[2])
if(len(sys.argv) > 3): game = sys.argv[3].lower()
with open("%s" % sys.argv[1]) as f:
    for line in f:
        if((l:=line.strip().lower()).isalpha() and (wordlen:=len(l)) >= minlen):                #> or >=
            if(l[:len(game)] == game): possibilities.add(l)
            dic.add(l)

getchildren(game)
print(len(pos_next_games))
input()

boardsfuture = getboardsfuture(game)
for letter, result in boardsfuture.items():
    if(result == 1): winners.add(letter.upper())
if(len(winners) == 0): print("Next player will lose!")
else: print(winners)