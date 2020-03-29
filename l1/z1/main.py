import time
import math
import functools
import sys
import random

class GaussianSteepestAscent:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def gen(self, size):
        random.seed()
        return [random.uniform(self.minimum, self.maximum) for _ in range(size)]

    def tweak(self, point, variance):
        newPoint = [x for x in point]

        for i, x in enumerate(newPoint):
            n = random.gauss(0, variance)
            while not (self.minimum <= x + n <= self.maximum):
                n = random.gauss(0, variance)
            newPoint[i] = x + n

        return newPoint

    def analyze(self, point, newPoint, f, variance):
        w = self.tweak(point, variance)
        if f(w) < f(newPoint):
            return w
        else:
            return newPoint

class LocalSearch:
    def __init__(self, f, candidate, time):
        super().__init__()
        self.f = f
        self.candidate = candidate
        self.time = time

    def find(self, n, sigma, tweakSigma):
        timeout = time.time() + self.time

        s = self.candidate.gen(4)
        best = s
        while timeout > time.time():
            r = self.candidate.tweak(s, sigma)
            for _ in range(n):
                if timeout <= time.time():
                    break
                r = self.candidate.analyze(s, r, self.f, tweakSigma)
            s = r
            if self.f(s) < self.f(best):
                best = s

        return best



def h(point):
    normsquare = sum(list(map(lambda x: x**2, point)))
    return pow((normsquare - 4) ** 2, 0.125) + 0.25 * (0.5 * normsquare + sum(point)) + 0.5

def g(point):
    return 1 + sum(map(lambda x: x**2/4000, point)) - functools.reduce(lambda x, y: x * math.cos(y[1] / math.sqrt(y[0] + 1)), enumerate(point), 1)

candidate = GaussianSteepestAscent(-2, 2)
params = input().split(" ")
t = int(params[0])
n = int(params[1])

if n == 0:
    f = h
    sigma = 1
    tweakSigma = 0.01
else:
    f = g
    sigma = 0.01
    tweakSigma = 0.00001
search = LocalSearch(f, candidate, t)

best = search.find(100, sigma, tweakSigma)

for x in best:
    print(x, end=' ')
print(f(best))
