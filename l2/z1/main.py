import time
import math
import functools
import sys
import random

def f(x):
    sumSqrt = math.sqrt(sum([xi*xi for xi in x]))
    return 1 - math.cos(2 * math.pi * sumSqrt) + 0.1 * sumSqrt

def tweak(solution, variance):
    newPoint = [x for x in solution]

    for i, x in enumerate(newPoint):
        newPoint[i] = x + random.gauss(0, variance) * x

    return newPoint

def simAnnealing(maxTime, initSolution, t, c, variance):
    timeout = time.time() + maxTime
    s = initSolution
    best = initSolution
    while timeout > time.time() and t > 0:
        r = tweak(s, variance)
        if f(r) < f(s) or random.random() < math.exp((f(s) - f(r)) / t):
            s = r
        t = t * c
        if f(s) < f(best):
            best = s
    return best


params = input().strip().split(" ")
t = int(params[0])
params = params[1:]
initSolution = [int(x) for x in params]
solution = simAnnealing(t, initSolution, 10, 0.997, 1)
print(f(solution))
print(solution)
