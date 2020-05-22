import random
import math
import time
import sys
from copy import deepcopy
from map import *
from path import *


def selectParent(population, path):
    t = 4
    best = random.choice(population)
    bestValue = path.cost(best)[0]
    for _ in range(t - 1):
        p = random.choice(population)
        if path.cost(p)[0] > bestValue:
            best = p
            bestValue = path.cost(p)[0]
    return best


def crossover(pa, pb):
    pa = list(pa)
    pb = list(pb)
    r = random.random()
    if r < 0.5:
        for i in range(min(len(pa), len(pb))):
            if random.random() < 0.3:
                pa[i], pb[i] = pb[i], pa[i]
    else:
        ia = random.randrange(0, len(pa))
        ib = random.randrange(0, len(pb))
        pa, pb = pa[:ia] + pb[ib:], pa[ia:] + pb[:ib]

    return ''.join(pa), ''.join(pb)


def ga(popsize, t, P, path):
    best = None
    bestValue = math.inf
    n = popsize // 2
    timeout = time.time() + t
    # print(P)
    lastbest = time.time()
    while timeout > time.time():
        P = sorted(P, key=lambda x: path.cost(x)[0])
        newValue, newBest = path.cost(P[0])
        if bestValue > newValue:
            bestValue, best = newValue, newBest
            lastbest = time.time()
        # print('after fitness')
        Q = P[:n]
        while len(Q) < popsize:
            pa = selectParent(P, path)
            pb = selectParent(P, path)
            # print(pa, pb)
            ca, cb = crossover(pa, pb)
            Q.append(path.mutate(ca))
            Q.append(path.mutate(cb))
        P = Q[:popsize]
        if (time.time() - lastbest) > math.log(t) * 2:
            return best, bestValue

    return best, bestValue


t, n, m, s, p = (int(x) for x in input().split(" "))
labyrinth = [list(map(lambda x: int(x), input())) for _ in range(n)]
initPopulation = [input().strip() for _ in range(s)]
lab = Map(labyrinth)
path = Path(lab)

path, cost = ga(p, t, initPopulation, path)
print(len(path))
print(path, file=sys.stderr)