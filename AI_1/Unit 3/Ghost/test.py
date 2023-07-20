import sys
import math
worddict = "words_all.txt"
inputWord = "ab" #sys.argv[1]
minWordLength = 4 #sys.argv[2]
word_list = []
opp = {1:2, 2:1}
with open(worddict) as f:
  word_list = [word.rstrip().lower() for word in f if len(word.rstrip()) >= minWordLength and word.rstrip().isalpha()]
curr_root = ''


def possibleMoves(currWord):
  curr_branch = tree
  for c in currWord:
    curr_branch = curr_branch[c]
  return list(curr_branch.keys())

def gameover(word):
  if word in word_list:
    return True
  return False

def score(word, player):
  if (len(word) - len(inputWord)) % 2 == 0:
    return 1
  else:
    return -1
#isalpha()

def make_tree(word_list):
  for word in word_list:
    if word.isalpha() and len(word) >= minWordLength:
      curr_branch = tree
      for c in word: 
        if c in curr_branch.keys():
          curr_branch = curr_branch[c]
        else:
          curr_branch[c] = {}
          curr_branch = curr_branch[c]

def find_solutions(word, min_depth):
  curr_branch = tree
  for c in word:  
    curr_branch = curr_branch[c]
  results = []
  for key in curr_branch.keys():
    temp = recur(curr_branch[key], 1)
    if temp is not None and temp%2 == 1:
      results.append(key)
  return results

def recur(curr_branch, depth):
  if len(curr_branch) == 0:
    return depth
  for key in curr_branch.keys():
    return recur(curr_branch[key], depth+1)

def minimax(word, player, alpha, beta):
  if gameover(word):
    return score(word, player)
  if player == 1:
    #do maxstep
    maxScore = -math.inf
    for possMove in possibleMoves(word):
      child = word + possMove
      result = minimax(child, opp[player], alpha, beta)
      maxScore = max(maxScore, result)
      alpha = max(alpha, result)
      if beta <= alpha:
        break
    return maxScore
  else:
    #do minstep
    minScore = math.inf
    for possMove in possibleMoves(word):
      child = word + possMove
      result = minimax(child, opp[player], alpha, beta)
      minScore = min(minScore, result)
      beta = min(beta, result)
      if beta <= alpha:
        break
    return minScore

tree = {}
make_tree(word_list)
winningMoves = []

for possMove in possibleMoves(inputWord):
  child = inputWord + possMove
  result = minimax(child, 2, -math.inf, math.inf)
  print(f"child: {child}   result: {result}")
  input()
  if result == 1:
    winningMoves.append(possMove)

if len(winningMoves) == 0:
  print("The next player loses!")
else:
  print(winningMoves)


print('********')
#print(tree['a']['b'])
#print(possibleMoves("aby")