from re import A
import sys
import numpy as np
import math
from math import sin

#Functions
def functionA(vec):
    x, y = vec[0], vec[1]
    return (4*(x**2)) - (3*x*y) + (2*(y**2)) + (24*x) - (20*y)
def gradA(vec):                                     #returns dfA/dx, dfA/dy
    x, y = vec[0], vec[1]
    return np.array([(8*x) - (3*y) + 24, (-3*x) + (4*y) - 20])

def functionB(vec):
    x, y = vec[0], vec[1]
    return (1-y)**2 + (x-y**2)**2
def gradB(vec):                                     #returns dfB/dx, dfB/dy
    x, y = vec[0], vec[1]
    return np.array([2*(x-y**2), (-4*x*y) + (4*(y**3))+ (2*y) - 2])
#def f(x): return sin(x) + sin(3*x) + sin(4*x)

#Global Variables
LOCAL_MIN = 10**(-8)
LAMBDA = 0.1
if(sys.argv[1] == "A"): FUNCTION, GRADF = functionA, gradA          #A or B; Function A: 4x^2 - 3xy + 2y^2 + 24x - 20y; Function B: (1-y)^2 + (x-y^2)^2
elif(sys.argv[1] == "B"): FUNCTION, GRADF = functionB, gradB
START = np.array([0.0, 0.0])

def magnitude(vec):                       #input: gradient_vector; returns magnitude of vector
    return np.linalg.norm(vec)

def findMin(f, gradf):                     #f and gradf are the actual function calls
    pos = START                             #pos is a np.array vector
    gvec = gradf(pos)                       #gvec is a np.array vector
    print(f"location: {pos}     gradient_vector: {gvec}")
    while(magnitude(gvec) >= LOCAL_MIN):
        pos -= LAMBDA * gvec
        gvec = gradf(pos)
        print(f"location: {pos}     gradient_vector: {gvec}")
    return f(pos)

findMin(FUNCTION, GRADF)
#A takes 75 iterations
#B takes 490 iterations


'''
The algorithm here is to choose a learning rate, λ, and then:
• Calculate the opposite of the gradient at the current location. This vector represents the direction to move to
achieve the steepest descent from the current location.
• Take the current position and add λ times the negative gradient. In other words, if we represent the position
after n steps as the vector xn, we are saying xn = xn−1 − λ∇f(xn−1

) This represents making a small step in the

direction of the negative gradient vector.
• Repeat until you get acceptably close to a local minimum.
'''