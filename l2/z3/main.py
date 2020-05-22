import random
import math
import time
import sys
from copy import deepcopy
from map import *
from path import *

def simAnnealing(maxTime, t, c, path):
    timeout = time.time() + maxTime
    s = path.initPath()
    bestcost, best = path.cost(s)
    lastbest = time.time()
    while timeout > time.time() and t > 0:
        r = path.tweak(s)
        rcost, r = path.cost(r)
        scost, s = path.cost(s)
        if rcost < scost or random.random() < math.exp((scost - rcost) / t):
            s = r
        t = t * c
        if scost < bestcost:
            best = s
            bestcost = scost
            lastbest = time.time()
        if (time.time() - lastbest) > math.log(maxTime) * 2:
            return best, bestcost

    return best, bestcost

t, n, m = (int(x) for x in input().split(" "))
labyrinth = [list(map(lambda x: int(x), input())) for _ in range(n)]
lab = Map(labyrinth)
path = NaivePath(lab)
path, cost = simAnnealing(t, 10 ** 4, 0.99, path)
print(len(path))
print(path, file=sys.stderr)