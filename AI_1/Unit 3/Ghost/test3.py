dic = {}
s = {"abalones"}
game = "ab"

def addtodic(dic, key, val):
    if key not in dic: dic.update({key : {val}})
    else: dic[key].add(val)

def process(dic, s, game):         #set of possible moves
    for word in s:
        partial_games = []
        for i in range((len(game)), len(word)): partial_games.append(word[:i])
        for i in range(len(partial_games)-1):
            addtodic(dic, partial_games[i], partial_games[i+1])

process(dic, s, game)
print(s)
print(dic)