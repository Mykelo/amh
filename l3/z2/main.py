import time
import math
import random
from copy import copy, deepcopy
import sys


def fitness(p, letters, dictionary):
    if not isValid(p, letters) or p not in dictionary:
        return 0
    return sum([letters[pi][0] for pi in p])

def isValid(p, letters):
    d = {}
    for c in p:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1

    return all([c in letters and d[c] <= letters[c][1] for c in d.keys()])

def selectParent(population, letters, dictionary):
    t = 7
    best = random.choice(population)
    bestValue = fitness(best, letters, dictionary)
    for _ in range(t - 1):
        p = random.choice(population)
        if fitness(p, letters, dictionary) > bestValue:
            best = p
            bestValue = fitness(p, letters, dictionary)
    return best

def twoPointCrossover(pa, pb):
    i1a, i2a = random.choices(range(len(pa)), k=2)
    i1b, i2b = random.choices(range(len(pb)), k=2)

    if i1a > i2a:
        i1a, i2a = i2a, i1a

    if i1b > i2b:
        i1b, i2b = i2b, i1b
    
    return pa[:i1a] + pb[i1b:i2b] + pa[i2a:], pb[:i1b] + pa[i1a:i2a] + pb[i2b:]

def onePointCrossover(pa, pb):
    pass

def crossover(pa, pb):
    r = random.random()
    if r < 0.5:
        return twoPointCrossover(pa, pb)
    newpa = list(pa)
    newpb = list(pb)
    l = min(len(newpa), len(newpb))
    for i in range(l):
        if random.random() < 1 / l:
            newpa[i], newpb[i] = newpb[i], newpa[i]

    return ''.join(newpa), ''.join(newpb)


def mutate(p, letters):
    if random.random() < 0.5:
        return p
    r = random.random()
    if r < 0.3:
        return p + ''.join(random.choices(letters, k=(random.randint(1, 2))))
    if r < 0.6:
        i = random.randrange(0, len(p))
        return p[:i] + ''.join(random.choices(letters, k=(random.randint(1, 2)))) + p[i:]
    if r < 0.8:
        p = list(p)
        i1, i2 = random.choices(range(len(p)), k=2)
        p[i1], p[i2] = p[i2], p[i1]
        return ''.join(p)
    if r < 1:
        p = list(p)
        for i in range(len(p)):
            if random.random() < 0.2:
                p[i] = random.choice(letters)
        return ''.join(p)
    return p


def getLettersList(letters):
    lettersList = []
    for k in letters:
        lettersList += [k] * letters[k][1]
    return lettersList


def genIndividual(allowedSollutions, letters):
    random.shuffle(letters)
    return ''.join(letters[:random.randrange(1, len(letters))])


def ga(popsize, t, dictionary, letters, allowedSollutions):
    lettersList = getLettersList(letters)
    P = list(allowedSollutions.keys())[:popsize]
    while len(P) < popsize:
        P.append(genIndividual(allowedSollutions, lettersList))
    best = None
    bestValue = 0
    timeout = time.time() + t
    lastbest = time.time()
    n = popsize // 2
    while timeout > time.time():
        allowed = [p for p in P if p in dictionary and isValid(p, letters)]
        allowed = list(set(allowed))
        allowed = sorted(allowed, key=lambda x: fitness(x, letters, dictionary), reverse=True)
        newValue = fitness(allowed[0], letters, dictionary)
        if best == None or newValue > bestValue:
            best = allowed[0]
            bestValue = newValue
            lastbest = time.time()
        Q = allowed[:n]
        while len(Q) < popsize:
            pa = selectParent(P, letters, dictionary)
            pb = selectParent(P, letters, dictionary)
            ca, cb = crossover(pa, pb)
            Q.append(mutate(ca, lettersList))
            Q.append(mutate(cb, lettersList))
        P = Q[:popsize]
        if (time.time() - lastbest) > math.log(t + 1) * 2:
            return best, bestValue

    return best, bestValue

params = [int(x) for x in input().strip().split(" ")]
t, n, s = params

letters = {}
for _ in range(n):
    c, p = input().strip().split(" ")
    if c in letters:
        letters[c][1] += 1
    else:
        letters[c] = [int(p), 1]

allowedSollutions = {}
for _ in range(s):
    allowedSollutions[input().lower()] = True

dictionary = {}
dictFile = open('dict.txt', 'r')

for line in dictFile.readlines():
    dictionary[line.strip().lower()] = True

best, value = ga(20, t, dictionary, letters, allowedSollutions)
print(value)
print(best, file=sys.stderr)