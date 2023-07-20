def f(a):
    return a[1]

def g(a):
    return (-a[0], a[1])

# Use of lambda to write a short function and name it h
h = lambda a: a[1]

x = [(1, "A"), (0, "C"), (2, "B"), (1, "D")]

# Various examples of using sorting keys, including directly using
# a lambda function
print(f(x))
print(h(x))

print(sorted(x, key=f))
print(sorted(x, key=g))
print(sorted(x, key=h))
print(sorted(x, key=lambda a: a[1]))