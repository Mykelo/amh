import time
import math
import random

def f(x, randomVariables):
    return sum([randomVariables[i] * (abs(x[i]) ** (i + 1)) for i in range(len(x))])

class Particle:
    def __init__(self, x, variance, size, f):
        self.x = x
        self.bestX = x
        self.bestValue = f(x)
        self.f = f
        self.velocity = [random.gauss(0, variance) for _ in range(size)]
        self.bestInformantX = [0] * size
        self.bestInformantXValue = math.inf
        self.particlesToInform = []
        self.size = size

    def assessFitness(self):
        value = self.f(self.x)
        if value < self.bestValue:
            self.bestX = self.x
            self.bestValue = value
            self.informOthers()
    
    def addObserver(self, observer):
        self.particlesToInform.append(observer)

    def informOthers(self):
        for observer in self.particlesToInform:
            observer.updateBest(self.bestX, self.bestValue)

    def updateBest(self, x, value):
        if value < self.bestInformantXValue:
            self.bestInformantXValue = value
            self.bestInformantX = x

    def updatePosition(self, globalBest, alfa, beta, gamma, delta, epsilon):
        # print(globalBest, end=' ')
        for i in range(self.size):
            b = random.uniform(0, beta)
            c = random.uniform(0, gamma)
            d = random.uniform(0, delta)
            vi = alfa * self.velocity[i] + b * (self.bestX[i] - self.x[i]) + c * (self.bestInformantX[i] - self.x[i]) + d * (globalBest[i] - self.x[i])
            self.x[i] += epsilon * vi
        # print(globalBest)
    

def particleSwarm(initSolution, randomVariables, swarmsize, alfa, beta, gamma, delta, epsilon, t):
    random.seed()
    currF = lambda x: f(x, randomVariables)
    swarm = [Particle(initSolution, 0.05, 5, currF)]
    for _ in range(swarmsize):
        x = [random.gauss(xi, 7) for xi in initSolution]
        swarm.append(Particle(x, 0.05, 5, currF))

    # Assign random particles to inform
    for p in swarm:
        for i in random.choices(swarm, k=(swarmsize // 3)):
            i.addObserver(p)

    timeout = time.time() + t
    best = initSolution
    bestValue = currF(initSolution)
    lastbest = time.time()
    while timeout > time.time():
        for p in swarm:
            p.assessFitness()
            if p.bestValue < bestValue:
                bestValue = p.bestValue
                best = [xi for xi in p.bestX]
                lastbest = time.time()
        for p in swarm:
            p.updatePosition(best, alfa, beta, gamma, delta, epsilon)
        if (time.time() - lastbest) > math.log(t + 1) * 2:
            return best, bestValue

    return best, bestValue




params = input().strip().split(" ")
t = int(params[0])
params = params[1:]
initSolution = [int(x) for x in params[:5]]
randomVariables = [float(x) for x in params[5:]]

solution, value = particleSwarm(initSolution, randomVariables, 100, 0.5, 0.2, 1, 0.5, 1, t)
for b in solution:
    print(b, end=' ')
print(value)