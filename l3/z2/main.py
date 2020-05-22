import time
import math
import random
from copy import copy, deepcopy
import sys


def fitness(p, letters):
    return sum([letters[pi] for pi in p])


def selectParent(population, letters):
    t = 4
    best = random.choice(population)
    bestValue = fitness(best, letters)
    for _ in range(t - 1):
        p = random.choice(population)
        if fitness(p, letters) > bestValue:
            best = p
            bestValue = fitness(p, letters)
    return best


def crossover(pa, pb):
    ia = random.randrange(0, len(pa))
    ib = random.randrange(0, len(pb))
    newpa, newpb = pa[:ia] + pb[ib:], pa[ia:] + pb[:ib]
    newpa = list(newpa)
    newpb = list(newpb)
    for i in range(min(len(newpa), len(newpb))):
        if random.random() < 0.2:
            newpa[i], newpb[i] = newpb[i], newpa[i]

    return ''.join(newpa), ''.join(newpb)


def mutate(p, letters):
    if random.random() < 0.8:
        return p
    r = random.random()
    if r < 0.2:
        return p + ''.join(random.choices(letters, k=(random.randint(1, 2))))
    if r < 0.6:
        i = random.randrange(0, len(p))
        return p[:i] + ''.join(random.choices(letters, k=(random.randint(1, 2)))) + p[i:]
    if r < 1:
        p = list(p)
        for i in range(len(p)):
            if random.random() < 0.1:
                p[i] = random.choice(letters)
        return ''.join(p)
    return p


def genIndividual(allowedSollutions, letters, maxSize):
    individual = ''
    for _ in range(random.randrange(maxSize // 2, maxSize)):
        individual += random.choice(letters)
    
    return individual


def ga(popsize, t, dictionary, letters, allowedSollutions):
    lettersList = list(letters.keys())
    P = list(allowedSollutions.keys())[:popsize]
    while len(P) < popsize:
        P.append(genIndividual(allowedSollutions, lettersList, 10))
    best = None
    bestValue = 0
    timeout = time.time() + t
    lastbest = time.time()
    n = popsize // 2
    while timeout > time.time():
        allowed = [p for p in P if p in dictionary]
        allowed = list(set(allowed))
        allowed = sorted(allowed, key=lambda x: fitness(x, letters), reverse=True)
        newValue = fitness(allowed[0], letters)
        if best == None or newValue > bestValue:
            best = allowed[0]
            bestValue = newValue
            lastbest = time.time()
        Q = allowed[:n]
        while len(Q) < popsize:
            pa = selectParent(allowed, letters)
            pb = selectParent(allowed, letters)
            ca, cb = crossover(pa, pb)
            Q.append(mutate(ca, lettersList))
            Q.append(mutate(cb, lettersList))
        P = Q[:popsize]
        if (time.time() - lastbest) > math.log(t) * 2:
            return best, bestValue

    return best, bestValue

params = [int(x) for x in input().strip().split(" ")]
t, n, s = params

letters = {}
for _ in range(n):
    c, p = input().strip().split(" ")
    letters[c] = int(p)

allowedSollutions = {}
for _ in range(s):
    allowedSollutions[input().lower()] = True

dictionary = {}
dictFile = open('dict.txt', 'r')

for line in dictFile.readlines():
    dictionary[line.strip().lower()] = True

# b = 0
# bs = ''
# for d in dictionary.keys():
#     if all([s in letters for s in d]) and fitness(d, letters) > b:
#         b = fitness(d, letters)
#         bs = d

# print(bs, b)

best, value = ga(40, t, dictionary, letters, allowedSollutions)
print(value)
print(best, file=sys.stderr)