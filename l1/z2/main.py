import sys
import random
import time
import itertools

class TSPTabu:
    def __init__(self, distances, tabulen, duration):
        self.tabu = []
        self.tabulen = tabulen
        self.duration = duration
        self.distances = distances

    def tweak(self, s):
        l = len(s)
        scopy = [x for x in s]
        x = random.randrange(1, l)
        y = random.randrange(1, l)
        while x == y:
            x = random.randrange(1, l)
            y = random.randrange(1, l)

        scopy[x], scopy[y] = scopy[y], scopy[x]
        return scopy

    def tweak2(self, s, x, y):
        scopy = [x for x in s]
        scopy[x], scopy[y] = scopy[y], scopy[x]
        return scopy

    def cost(self, s):
        l = len(s)
        d = [self.distances[s[i]][s[(i + 1) % l]] for i in range(l)]
        return sum(d)

    def genNew(self):
        s = [x + 1 for x in range(len(self.distances) - 1)]
        random.shuffle(s)
        s = [0] + s
        return s

    def find(self, n):
        random.seed()
        s = self.genNew()
        comb = list(itertools.combinations([x + 1 for x in range(len(self.distances) - 1)], 2))

        timeout = time.time() + self.duration
        best = s
        while timeout > time.time():
            if len(self.tabu) > self.tabulen:
                self.tabu = self.tabu[1:]
            r = self.genNew()
            # for _ in range(n - 1):
            #     w = self.tweak(s)
            random.shuffle(comb)
            for x in comb:
                w = self.tweak2(s, x[0], x[1])
                if w not in self.tabu and (self.cost(w) < self.cost(r) or r in self.tabu):
                    r = w
            if r not in self.tabu:
                s = r
                self.tabu.append(r)
            if self.cost(s) < self.cost(best):
                best = s

        return best


params = input().split(" ")
t = int(params[0])
n = int(params[1])

distances = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    cityDistances = map(lambda x: float(x), input().split(" "))
    for j, x in enumerate(cityDistances):
        if j != i:
            distances[i][j] = x


search = TSPTabu(distances, 10 * n, t)
best = search.find(n * (n - 1) / 2)

print(best, search.cost(best))
