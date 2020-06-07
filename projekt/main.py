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
    l = min(len(pa), len(pb))
    if r < 0.5:
        for i in range(l):
            if random.random() < 1 / l:
                pa[i], pb[i] = pb[i], pa[i]
    else:
        ia = random.randrange(0, len(pa))
        ib = random.randrange(0, len(pb))
        pa, pb = pa[:ia] + pb[ib:], pa[ia:] + pb[:ib]

    return ''.join(pa), ''.join(pb)


def getDiff(x1, x2):
    value1, _, pos1 = x1
    value2, _, pos2, = x2
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 - abs(value1 - value2)


def ga(popsize, t, P, path):
    best = None
    bestValue = math.inf
    bestPos = (0, 0)
    nBest = popsize // 3
    nWorst = popsize // 4
    timeout = time.time() + t
    lastbest = time.time()
    for _ in range(popsize - 1):
        P.append(path.mutate(P[0]))
    while timeout > time.time():
        calculatedP = list(map(path.cost, P))
        P = [p[1] for p in sorted(calculatedP, key=lambda x: x[0])]
        newValue, newBest, newPos = calculatedP[0]
        if bestValue > newValue:
            bestValue, best, bestPos = newValue, newBest, newPos
            lastbest = time.time()
        farthest = [p[1] for p in sorted(calculatedP, key=lambda x: getDiff((bestValue, best, bestPos), x), reverse=True)]
        # print(P)
        # print(farthest)
        # print()
        Q = P[:nBest]
        Q += farthest[:nWorst]
        while len(Q) < popsize:
            pa = selectParent(P, path)
            pb = selectParent(P, path)
            ca, cb = crossover(pa, pb)
            Q.append(path.mutate(ca))
            Q.append(path.mutate(cb))
        P = Q[:popsize]
        if (time.time() - lastbest) > math.log(t + 1) * 2:
            return best, bestValue

    return best, bestValue


def simAnnealing(maxTime, t, c, path, initSolution):
    # random.seed(17)
    timeout = time.time() + maxTime
    s = initSolution
    bestcost, best, _ = path.cost(s)
    lastbest = time.time()
    while timeout > time.time() and t > 0:
        r = path.tweak(s)
        rcost, r, _ = path.cost(r)
        scost, s, _ = path.cost(s)
        if rcost < scost or random.random() < math.exp((scost - rcost) / t):
            s = r
        t = t * c
        if scost < bestcost:
            best = s
            bestcost = scost
            lastbest = time.time()
        if (time.time() - lastbest) > math.log(maxTime + 1):
            return best, bestcost

    return best, bestcost


t, n, m = (int(x) for x in input().split(" "))
labyrinth = [list(map(lambda x: int(x), input())) for _ in range(n)]
initSolution = input().strip()
lab = Map(labyrinth)
path = Path(lab)

# l, path, d = path.cost('LLULUUUUUU')
# path, cost = ga(20, t, initPopulation, path)
maxTime = min(t, n + m)
path, cost = simAnnealing(maxTime, 10 ** 3, 0.99, path, initSolution)
print(len(path))
print(path, file=sys.stderr)