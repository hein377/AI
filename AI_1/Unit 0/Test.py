import sys
#print(sys.argv)
#print(sys.argv[1])

def summed(x):
    s = 0
    for i in list(str(x)): s += int(i)**5
    return s

ls = [x for x in range(2,1000000) if x==summed(x)]
print("30: %s" % (sum(ls)))