import sys; args = sys.argv[1:]
idx = int(args[0])-50

myRegexLst = [
  r"/\w*(\w)\w*\1\w*/i",
  r"/\w*(\w)(\w*\1){3}\w*/i",
  r"/^(0|1|([01])[01]*\2)$/",
  r"/\b(?=\w*cat)\w{6}\b/i",
  r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
  r"/\b(?!\w*cat)\w{6}\b/i",
  r"/\b(?!\w*(\w)\w*\1)\w+/i",
  r"/^(?![10]*10011)[01]*$/",
  r"/\w*([aeiou])(?=[aeiou])(?!\1)\w*/i",
  r"/^(?![10]*(101|111))[01]*$/",
]

if idx < len(myRegexLst):
  print(myRegexLst[idx])
#Hein Htut 3 2023
'''
Q50: Match all words where some letter appears twice in the same word.
Q51: Match all words where some letter appears four times in the same word.
Q52: Match all non-empty binary strings with the same number of 01 substrings as 10 substrings.
Q53: Match all six letter words containing the substring cat.
Q54: Match all 5 to 9 letter words containing both the substrings bri and ing.
Q55: Match all six letter words not containing the substring cat.
Q56: Match all words with no repeated characters.
Q57: Match all binary strings not containing the forbidden substring 10011.
Q58: Match all words having two different adjacent vowels.
Q59: Match all binary strings containing neither 101 nor 111 as substrings.
'''