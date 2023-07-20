import random
import numpy as np

def generatexy(n):
    return [np.array([[random.uniform(-1, 1), (random.uniform(-1, 1))]]) for i in range(n)]

print(generatexy(50))
print(type(generatexy(5)[0]))