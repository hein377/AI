import sys
import re

#Global Variables
global dic
dic = []
maxstringlen = 0

#Setting up dic
with open("%s" % sys.argv[1]) as f:
    for line in f: 
        s = line.strip().lower()
        if len(s) > maxstringlen: maxstringlen = len(s)
        dic.append(s)

def printsol(solutions, l):
    if(l > 5): l = 5
    for i in range(l): print(solutions[i])
    print()

def reg1():
    solutions, matches, min, reg = [], [], 100, re.compile(r"\b(?=\w*a)(?=\w*e)(?=\w*i)(?=\w*o)(?=\w*u)\w*\b")
    for word in dic:
        for result in reg.finditer(word): 
            if(len(result.string) < min): min = len(result.string)
            matches.append(result.string)
    for candidate in matches:
        if(len(candidate) == min): solutions.append(candidate)
    solutions.sort()

    print(f"#1: {reg}")
    print(f"{len(solutions)} total matches")
    printsol(solutions, len(solutions))

def reg2():
    solutions, matches, max, reg = [], [], 0, re.compile(r"\b([^aeiou]*[aeiou]){5}[^aeiou]*\b")
    for word in dic:
        for result in reg.finditer(word): 
            if(len(result.string) > max): max = len(result.string)
            matches.append(result.string)
    for candidate in matches:
        if(len(candidate) == max): solutions.append(candidate)
    solutions.sort()

    print(f"#2: {reg}")
    print(f"{len(solutions)} total matches")
    printsol(solutions, len(solutions))

def reg3():
    solutions, matches, max, reg = [], [], 0, re.compile(r"\b(\w)(?!\w*\1\w)\w*\1\b")
    for word in dic:
        for result in reg.finditer(word): 
            if(len(result.string) > max): max = len(result.string)
            matches.append(result.string)
    for candidate in matches:
        if(len(candidate) == max): solutions.append(candidate)
    solutions.sort()

    print(f"#3: {reg}")
    print(f"{len(solutions)} total matches")
    printsol(solutions, len(solutions))

def reg4():
    reg = re.compile(r"\b(\w)(\w)(\w)\w*\b(?<=\3\2\1)")
    solutions = list(filter(reg.match, dic))
    solutions.sort()

    print(f"#4: {reg}")
    print(f"{len(solutions)} total matches")
    printsol(solutions, len(solutions))

def reg5():
    only_one_tb, reg1, reg2 = [], re.compile(r"^(?!\w*t\w*t)(?!\w*b\w*b)\w*"), re.compile(r"\w*(tb|bt)\w*")
    only_one_tb = list(filter(reg1.match, dic))
    solutions = list(filter(reg2.match, only_one_tb))
    solutions.sort()

    print(f"#5: {reg1}, {reg2}")
    print(f"{len(solutions)} total matches")
    printsol(solutions, len(solutions))

def reg6():
    k = 1
    reg = re.compile(r"^\w*(\w)\1{" + str(k) + r"}\w*$")
    matches = list(filter(reg.match, dic))
    while(len(matches) != 0):
        k+=1
        reg = re.compile(r"^\w*(\w)\1{" + str(k) + r"}\w*$")
        if(len(search:=list(filter(reg.match, dic)))!=0): matches = search
        else: break

    print(f"#6: {reg}")
    print(f"{len(matches)} total matches")
    printsol(matches, len(matches))

def reg7():
    k = 1
    reg = re.compile(r"^\w*(\w)(\w*(\1)){" + str(k) + r"}\w*$")
    matches = list(filter(reg.match, dic))
    while(len(matches) != 0):
        k+=1
        reg = re.compile(r"^\w*(\w)(\w*(\1)){" + str(k) + r"}\w*$")
        if(len(search:=list(filter(reg.match, dic)))!=0): matches = search
        else: break

    print(f"#7: {reg}")
    print(f"{len(matches)} total matches")
    printsol(matches, len(matches))

def reg8():
    k = 1
    reg = re.compile(r"^\w*(\w\w)(\w*\1){" + str(k) + r"}\w*$")
    matches = list(filter(reg.match, dic))
    while(len(matches) != 0):
        k+=1
        reg = re.compile(r"^\w*(\w\w)(\w*\1){" + str(k) + r"}\w*$")
        if(len(search:=list(filter(reg.match, dic)))!=0): matches = search
        else: break

    print(f"#8: {reg}")
    print(f"{len(matches)} total matches")
    printsol(matches, len(matches))

def reg9():
    k = 1
    reg = re.compile(r"^(\w*[b-df-hj-np-tv-z]){" + str(k) + r"}\w*$")
    matches = list(filter(reg.match, dic))
    while(len(matches) != 0):
        k+=1
        reg = re.compile(r"^(\w*[b-df-hj-np-tv-z]){" + str(k) + r"}\w*$")
        if(len(search:=list(filter(reg.match, dic)))!=0): matches = search
        else: break

    print(f"#9: {reg}")
    print(f"{len(matches)} total matches")
    printsol(matches, len(matches))

def reg10():
    solutions, matches, max, reg = [], [], 0, re.compile(r"^(?!\w*(\w)(\w*\1){2})\w*$")
    for word in dic:
        for result in reg.finditer(word): 
            if(len(result.string) > max): max = len(result.string)
            matches.append(result.string)
    for candidate in matches:
        if(len(candidate) == max): solutions.append(candidate)
    solutions.sort()

    print(f"#10: {reg}")
    print(f"{len(solutions)} total matches")
    printsol(solutions, len(solutions))

for i in range(1, 11): eval(f"reg{i}()")

"""
Sample Regex: exp3 = re.compile(r"..l", re.I | re.S | re.M)

Prompts:
1) Match all words of minimum length that contain each vowel at least once. (That is, from all of the words that
contain each vowel at least once, find the shortest length and output the number of matching words of that
length, ignoring the rest. Then print up to the first five of them, in alphabetical order. You don’t need to use a
regex to filter by length; you do need to use a regex to find the words in the first place.)
2) Match all words of maximum length that contain precisely 5 vowels. (Same additional instructions as #1.)
3) Match all words of maximum length where the first letter reappears as the last letter but does not appear
anywhere else in the word. (Same additional instructions as #1.)
4) Match all words where the first three letters, reversed, are the last three letters. Overlapping is ok; for instance,
"ada" and "abba" should both count.
5) Match all words where there is exactly one “b”, exactly one “t”, and they are adjacent to each other.
6) Match all words with the longest contiguous block of a single letter. (That is, figure out what the longest
contiguous block of a single letter is, and print out all words with a block of that length. This may require more
than one regex to find, or a loop modifying and re-searching with a series of regexes.)
7) Match all words with the greatest number of a repeated letter (which may occur anywhere in the word). Same
additional instructions as #6.
8) Match all words with the greatest number of adjacent pairs of identical letters. Order matters; that is, "ab" is
not the same pair as "ba". Same additional instructions as #6.
9) Match all words with the greatest number of consonants. Same additional instructions as #6.
10) Match all words of maximum length where no letter is repeated more than once. (That is, where no letter
appears more than twice!)

Output Sample:
#1 re.compile(YOUR REGEX GOES HERE)
16 total matches
word
word
word
word
word
(leave a blank space before the next question)
"""