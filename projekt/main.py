import random
import math
import time
import sys
from copy import deepcopy
from map import *
from path import *


def simAnnealing(maxTime, t, c, path, initSolution):
    timeout = time.time() + maxTime
    s = initSolution
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
        if (time.time() - lastbest) > math.log(maxTime + 1) / 2:
            return best, bestcost

    return best, bestcost


t, n, m = (int(x) for x in input().split(" "))
labyrinth = [list(map(lambda x: int(x), input())) for _ in range(n)]
initSolution = input().strip()
lab = Map(labyrinth)
path = Path(lab)

maxTime = min(t, n + m)
path, cost = simAnnealing(maxTime, 10 ** 3, 0.99, path, path.initPath())
print(len(path))
print(path, file=sys.stderr)