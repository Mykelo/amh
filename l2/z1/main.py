import time
import math
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
    lastbest = time.time()
    while timeout > time.time() and t > 0:
        r = tweak(s, variance)
        if f(r) < f(s) or random.random() < math.exp((f(s) - f(r)) / t):
            s = r
        t = t * c
        if (time.time() - lastbest) > math.log(maxTime) * 2:
            return best
        if f(s) < f(best):
            best = s
            lastbest = time.time()
    return best


params = input().strip().split(" ")
t = int(params[0])
params = params[1:]
initSolution = [int(x) for x in params]
solution = simAnnealing(t, initSolution, 10**9, 0.99, 1)

for x in solution:
    print(x, end=' ')
print(f(solution))
