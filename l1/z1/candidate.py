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
    def __init__(self, minimum, maximum, variance):
        Candidate.__init__(self, minimum, maximum)
        self.variance = variance

    def tweak(self, point):
        prob = 1.0
        newPoint = [x for x in point]
        variance = 5

        for i, x in enumerate(newPoint):
            if random.random() < prob:
                n = random.gauss(0, self.variance)
                while not (self.minimum <= x + n <= self.maximum):
                    n = random.gauss(0, self.variance)
                newPoint[i] = x + n

        return newPoint

    def analyze(self, point, newPoint, f):
        w = self.tweak(point)
        if abs(f(w)) < abs(f(newPoint)):
            return w
        else:
            return newPoint
                


