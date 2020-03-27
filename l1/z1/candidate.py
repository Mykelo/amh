import random

class Candidate:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def gen(self, size):
        random.seed()
        return [random.uniform(self.minimum, self.maximum) for _ in range(size)]

    def tweak(self, point):
        pass

    def analyze(self, point, newPoint, f):
        pass

class GaussianSteepestAscent(Candidate):
    def tweak(self, point, variance):
        prob = 1.0
        newPoint = [x for x in point]

        for i, x in enumerate(newPoint):
            if random.random() < prob:
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
                


