import sys

print("Blue Credit: \n")
def is_prime(x):
    for i in range(3, int(x**(1/2))+2, 2):
        if x % 2 == 0 or x % i == 0:
            return False
    return True

#a
print("a: " + str(sum({num1 for num1 in range(1000) if(num1 % 3 == 0 or num1 % 5 == 0)})))

#b
x, y = 0, 1
s = []
while(x + y < 4000000):
    n = x + y
    if(n % 2 == 0):
        s.append(n)
    x = y
    y = n
print("b: " + str(sum(s)))

#c
s = set(num1 for num1 in range(3, int(600851475143**(1/2))+1, 2) if 600851475143 % num1 == 0 and is_prime(num1))
print("c: " + str(max(s)))

#d
s = set(num1 * num2 for num1 in range(10, 1000) for num2 in range(100, 1000) if str(num1*num2)[:len(str(num1*num2))] == str(num1*num2)[:-len(str(num1*num2))-1:-1])
print("d: " + str(max(s)))

#e
def gcd(x,y):
    while(y != 0):
        t = y
        y = x % y
        x = t
    return x

def is_smallest_number(max, num):
    for i in range(3, max):
        if(gcd(i, num) != i): return False
    return True

def smallest_multiple(max):
    num = max + (max%2)
    while(not is_smallest_number(max, num)):
        num += max
    return num
print("e: " + str(smallest_multiple(20)))

#f
num1, num2 = 0, 0
for i in range(101):
    num1 += i**2
    num2 += i
print("f: " + str(num2**2-num1))

#g Find 10001st prime
num, count = 2, 0
while(count != 10001):
    if(is_prime(num)):
        count+=1
    num+=1
print("g: " + str(num-1))

#h
def maxi(str):
    prod = 1
    for i in list(str):
        prod *= int(i)
    return prod

def adjacent_product(x):
    s = str(x)
    ls = [maxi(s[i:i+13]) for i in range(len(s)-12) if '0' not in s[i:i+13]]
    return max(ls)

print("f: " + str(adjacent_product(7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450)))

#i
perfect_squares = {num1*num1 for num1 in range(1, 1000)}

#code for a dictionary of pythagorean triplets
dic = {}
for a in range(1, 100):
    for b in range(1, 100):
        c = (a**2 + b**2)
        if(c in perfect_squares):
            dic.update({c**0.5:[a, b]})

def rat():
    for a in range(1, 1000):
        for b in range(1, 1000):
            c = (a**2 + b**2)
            if(c in perfect_squares and a+b+(c**0.5)==1000.0):
                return int(a*b*(c**0.5))
print("i: " + str(rat()))

#j
s = {a**b for a in range(2, 101) for b in range(2, 101)}
print("j: " + str(len(s)) + "\n")

print("Red Credit: \n")
#11
matrix = [
[8,2,22,97,38,15,00,40,00,75,4,5,7,78,52,12,50,77,91,8],
[49,49,99,40,17,81,18,57,60,87,17,40,98,43,69,48,4,56,62,00],
[81,49,31,73,55,79,14,29,93,71,40,67,53,88,30,3,49,13,36,65],
[52,70,95,23,4,60,11,42,69,24,68,56,1,32,56,71,37,2,36,91],
[22,31,16,71,51,67,63,89,41,92,36,54,22,40,40,28,66,33,13,80],
[24,47,32,60,99,3,45,2,44,75,33,53,78,36,84,20,35,17,12,50],
[32,98,81,28,64,23,67,10,26,38,40,67,59,54,70,66,18,38,64,70],
[67,26,20,68,2,62,12,20,95,63,94,39,63,8,40,91,66,49,94,21],
[24,55,58,5,66,73,99,26,97,17,78,78,96,83,14,88,34,89,63,72],
[21,36,23,9,75,00,76,44,20,45,35,14,00,61,33,97,34,31,33,95],
[78,17,53,28,22,75,31,67,15,94,3,80,4,62,16,14,9,53,56,92],
[16,39,5,42,96,35,31,47,55,58,88,24,00,17,54,24,36,29,85,57],
[86,56,00,48,35,71,89,7,5,44,44,37,44,60,21,58,51,54,17,58],
[19,80,81,68,5,94,47,69,28,73,92,13,86,52,17,77,4,89,55,40],
[4,52,8,83,97,35,99,16,7,97,57,32,16,26,26,79,33,27,98,66],
[88,36,68,87,57,62,20,72,3,46,33,67,46,55,12,32,63,93,53,69],
[4,42,16,73,38,25,39,11,24,94,72,18,8,46,29,32,40,62,76,36],
[20,69,36,41,72,30,23,88,34,62,99,69,82,67,59,85,74,4,36,16],
[20,73,35,29,78,31,90,1,74,31,49,71,48,86,81,16,23,57,5,54],
[1,70,54,71,83,51,54,69,16,92,33,48,61,43,52,1,89,19,67,48],
]

def prod(ls):
    p = 1
    for i in ls: p *= int(i)
    return p
    
hmax = vmax = ddmax = dumax = 0
for row in range(len(matrix)):
    for col in range(len(matrix[row])):
        if(col <= 16):
            hprod = prod(matrix[row][col:col+4])
            if(hprod > hmax): hmax = hprod
        vls, ddls, duls = [], [], []
        for x in range(4):
            if(row <= 16):
                vls.append(matrix[row+x][col])
                if(col <= 16):
                    ddls.append(matrix[row+x][col+x])
            if(row >= 3 and col <= 16):
                duls.append(matrix[row-x][col+x])
        vprod, ddprod, duprod = prod(vls), prod(ddls), prod(duls)
        if(vprod > vmax): vmax = vprod
        if(ddprod > ddmax): ddmax = ddprod
        if(duprod > dumax): dumax = duprod
print("11: %s" % (max(max(max(hmax,vmax),ddmax),dumax)))


#12
def multiples(x):
    count = 0
    for i in range(1, int(x**0.5)+1):
        if(x % i == 0): count +=2
    if(int(x**0.5) * int(x**0.5) == x): count -= 1
    return count

x = 1
i = 2
while(multiples(x) < 500):
    x += i
    i+=1
print("12: %s" % (x))

#14
max_ind = max_len = 0
for i in range(3, 1000001):
    count, num = 1, i
    while(num != 1):
        if(num % 2 == 0): num = num//2
        else: num = 3*num + 1
        count+=1
    if(max_len < count): max_len, max_ind = count, i

print("14: %s" % (max_ind))

#21:
def d(x):
    s=0
    for i in range(1, x//2+1):
        if(x % i == 0): s+=i
    return s

dic, pairs = {}, []
for i in range(1, 10001):
    s = d(i)
    if(i in dic and s == dic.get(i) and s!=i): pairs.extend([i,s])
    else: dic.update({s:i})
print("21: %s" % (sum(pairs)))

#28
ls, su = [1], 1
for i in range(2, 1001, 2):
    for x in range(4):
        ls.append(s := ls[-1] + i)
        su += s

print("28: %s" % (su))

#30
def summed(x):
    s = 0
    for i in list(str(x)): s += int(i)**5
    return s

ls = [x for x in range(2,1000000) if x==summed(x)]
print("30: %s" % (sum(ls)))