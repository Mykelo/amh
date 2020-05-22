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
    r = random.random()
    if r < 0.2:
        return p + ''.join(random.choices(letters, k=(random.randint(0, len(p) // 2))))
    if r < 0.4:
        i = random.randrange(0, len(p))
        return p[:i] + ''.join(random.choices(letters, k=(random.randint(0, len(p) // 2)))) + p[i:]
    if r < 0.6:
        p = list(p)
        k = len(p) if len(p) == 1 else random.randrange(0, len(p) // 2)
        for i in random.choices(range(len(p)), k=k):
            p[i] = random.choice(letters)
        return ''.join(p)
    return p


def genIndividual(allowedSollutions, letters, maxSize):
    # p1, p2 = random.choices(allowedSollutions, k=2)
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
    # print(P)
    while timeout > time.time():
        # print(len(P))
        allowed = [p for p in P if p in dictionary]
        # print('after filtering')
        for p in allowed:
            newValue = fitness(p, letters)
            if (best == None or newValue > bestValue) and p in dictionary:
                best = p
                bestValue = newValue

        # print('after fitness')
        Q = []
        while len(Q) < popsize:
            pa = selectParent(allowed, letters)
            pb = selectParent(allowed, letters)
            # print(pa, pb)
            ca, cb = crossover(pa, pb)
            Q.append(mutate(ca, lettersList))
            Q.append(mutate(cb, lettersList))
        P = Q[:popsize]

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

# s = genIndividual(allowedSollutions, letters, 10)
# l = list(allowedSollutions.keys())
# s = selectParent(l, letters)
# s2 = selectParent(l, letters)
# print(s, s2, crossover(s, s2))

b = 0
bs = ''
for d in dictionary.keys():
    if all([s in letters for s in d]) and fitness(d, letters) > b:
        b = fitness(d, letters)
        bs = d

print(bs, b)

best, value = ga(100, t, dictionary, letters, allowedSollutions)
print(best, value)