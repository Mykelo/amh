from candidate import *
import time
import math
import functools

class LocalSearch:
    def __init__(self, f, candidate, time):
        super().__init__()
        self.f = f
        self.candidate = candidate
        self.time = time

    def find(self, n):
        timeout = time.time() + self.time

        s = self.candidate.gen(4)
        best = s
        while timeout > time.time():
            r = self.candidate.tweak(s)
            for _ in range(n):
                r = self.candidate.analyze(s, r, self.f)
            s = r
            if abs(self.f(s)) < abs(self.f(best)):
                best = s

        return best



def h(point):
    normsquare = sum(list(map(lambda x: x**2, point)))
    return pow(normsquare - 4, 0.25) + 0.25 * (0.5 * normsquare + sum(point)) + 0.5

def g(point):
    product = 1
    return 1 + sum(map(lambda x: x**2/4000, point)) - functools.reduce(lambda x, y: x * math.cos(y[1] / math.sqrt(y[0] + 1)), enumerate(point), 1)

candidate = GaussianSteepestAscent(-10, 10, 5)
search = LocalSearch(g, candidate, 2)

best = search.find(100)
print(best, g(best), abs(g(best)))

