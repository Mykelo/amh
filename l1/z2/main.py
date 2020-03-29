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

    def tweak(self, s, x, y):
        scopy = [x for x in s]
        scopy[x], scopy[y] = scopy[y], scopy[x]
        return scopy

    def largeTweak(self, s):
        a = random.randint(0, int(len(s) * 0.75))
        b = random.randint(a, len(s) - 1)
        scopy = [x for x in s]
        scopy[a:b] = list(reversed(scopy[a:b]))
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

    def initSolution(self):
        path = [0]
        while len(path) < len(self.distances):
            currCity = path[-1]
            nextCity = min([el for el in enumerate(self.distances[currCity]) if el[0] != x and el[0] not in path], key=lambda el: el[1])[0]
            path.append(nextCity)

        return path

    def find(self, n):
        random.seed()
        s = self.initSolution()
        comb = list(itertools.combinations([x + 1 for x in range(len(self.distances) - 1)], 2))
        timeout = time.time() + self.duration
        best = s
        while timeout > time.time():
            if len(self.tabu) > self.tabulen:
                self.tabu = self.tabu[1:]

            r = self.largeTweak(s)
            sample = random.sample(comb, n)
            for x in sample:
                if timeout <= time.time():
                    break
                w = self.tweak(s, x[0], x[1])
                if w not in self.tabu and (self.cost(w) < self.cost(r) or r in self.tabu):
                    r = w
            if r not in self.tabu:
                s = r
                self.tabu.append(r)
            if self.cost(s) < self.cost(best):
                best = s

        return best, self.cost(best)


params = input().split(" ")
t = int(params[0])
n = int(params[1])

distances = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    cityDistances = map(lambda x: float(x), input().split(" "))
    for j, x in enumerate(cityDistances):
        if j != i:
            distances[i][j] = x


search = TSPTabu(distances, 5 * n, t)
path = search.initSolution()
best, cost = search.find(int(n * (n - 1) / 3))

best.append(0)

print(cost)
print(" ".join([str(x) for x in best]), file=sys.stderr)
