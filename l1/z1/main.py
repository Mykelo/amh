from candidate import *
import time
import math
import functools
import sys

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
            r = self.candidate.tweak(s, 2)
            for _ in range(n):
                r = self.candidate.analyze(s, r, self.f, 0.1)
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
f = h if int(sys.argv[2]) == 0 else g
t = int(sys.argv[1])
search = LocalSearch(f, candidate, t)

best = search.find(200)

for x in best:
    print(x, end=' ')
print(f(best))

