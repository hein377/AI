import sys

if(sys.argv[1] == "A"):
    print(sum([int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])]))

if(sys.argv[1] == "B"):
    ls = []
    for i in sys.argv[2:]: ls.append(int(i))
    print(sum(ls))

if(sys.argv[1] == "C"):
    ls = []
    for i in sys.argv[2:]:
        if int(i) % 3 == 0:
            ls.append(i)
    print(ls)

if(sys.argv[1] == "D"):
    if(int(sys.argv[2]) >= 1):
        print("1")
    x, y = 0, 1
    for i in range(int(sys.argv[2])-1):
        n = x + y
        print((str)(n) + " ")
        x = y
        y = n

if(sys.argv[1] == "E"):
    def f(k):
        return k**2 - (3*k) + 2
    for i in range(int(sys.argv[2]), int(sys.argv[3])+1):
        print(f(i))

if(sys.argv[1] == "F"):
    arg1, arg2, arg3 = (float)(sys.argv[2]), (float)(sys.argv[3]), (float)(sys.argv[4])     #Tuple packing?
    def f(x, y, z):
        if (x+y<=z or x+z<=y or y+z<=x): return "Error" 
        s = (x+y+z)/2
        return ((s*(s-x)*(s-y)*(s-z))**(1/2))
    print(f(arg1, arg2, arg3))

if(sys.argv[1] == "G"):
    sys.argv[2].lower()
    print(["a"+(str)(sys.argv[2].count("a")), "e"+(str)(sys.argv[2].count("e")), "i"+(str)(sys.argv[2].count("i")), "o"+(str)(sys.argv[2].count("o")), "u"+(str)(sys.argv[2].count("u"))])