from colorama import init, Back, Fore  # Note I have imported specific things here
import sys, re
init()

def process(inputreg):
    if(lastslashind:=inputreg.rindex("/")) != (len(inputreg)-1):
        s = '", '
        for flag in list(inputreg[lastslashind+1:]):
            s += f"re.{flag.upper()} | "
        return 're.compile(r"' + inputreg[1:lastslashind] + s[:-3] + ")"
    return 're.compile(r"' + inputreg[1:lastslashind] + '")'

inputreg = sys.argv[1]
cur_color = "BLUE"              #Blue and Light Black
s = "While inside they wined and dined, safe from the howling wind.\nAnd she whined, it seemed, for the 100th time, into the ear of her friend,\nWhy indeed should I wind the clocks up, if they all run down in the end?"
print(process(inputreg))
reg = eval(process(inputreg))
#exp3 = re.compile(r"..l", re.I | re.S | re.M)

def changecolor(color):
    global cur_color
    if(color == "BLUE"): cur_color = "LIGHTBLACK_EX"
    if(color == "LIGHTBLACK_EX"): cur_color = "BLUE"

def printcolor(color, ind, startind, matched):
    print(s[ind:startind] + eval(f"Back.{color}") + matched + Back.RESET, end = "")

ind = 0
for match in reg.finditer(s):
    startind, endind = match.start(), match.end()
    if(startind == endind): print(s[ind:startind] + Fore.RED + "|" + Fore.RESET, end = "")
    elif ind == startind: 
        changecolor(cur_color)
        printcolor(cur_color, ind, startind, match[0])
    else: printcolor(cur_color, ind, startind, match[0])
    ind = endind
print(s[ind:])