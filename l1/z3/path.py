import random
from copy import deepcopy
import math

class Path:
    def __init__(self, m):
        self.map = m
        self.start = m.findStart()

    def initPath(self):
        return ""

    def move(self, pos, move):
        xdir, ydir = self.map.getDirection(move)
        newx, newy = (pos[0] + xdir, pos[1] + ydir)
        return (newx, newy) if self.map.map[newx][newy] == 0 else pos

    def cost(self, path):
        return 0

    def tweak(self, path):
        return ""

class NaivePath(Path):
    # Follow the walls to find the exit
    def initPath(self):
        path = ""
        directionsOrder = ["D", "L", "U", "R"]
        currDir = 0
        pos = deepcopy(self.start)
        while not self.map.checkExit(pos):
            newpos = self.move(pos, directionsOrder[currDir])
            if newpos == pos:
                currDir = (currDir + 1) % 4
            else:
                pos = newpos
                path += directionsOrder[currDir]
        return path

    def cost(self, path):
        if self.map.checkExit(self.start) or len(path) == 0: return 0

        pos = deepcopy(self.start)
        cost = 1
        for step in path:
            newpos = self.move(pos, step)
            if newpos == pos:
                return math.inf, path
            cost += 1
            if self.map.checkExit(newpos):
                return cost, path[0:cost]
            pos = newpos
        return math.inf, path

    # Swap random pair of elements
    def tweak(self, path):
        l = len(path)
        copy = [x for x in path]
        x = random.randrange(0, l)
        y = random.randrange(0, l)
        while x == y:
            x = random.randrange(0, l)
            y = random.randrange(0, l)
        copy[x], copy[y] = copy[y], copy[x]
        return "".join(copy)

class NaivePathV2(NaivePath):
    def tweak(self, path):
        copy = [x for x in path]
        l = len(copy)
        # Swap random number of random pairs
        for _ in range(random.randrange(1, int(l / 5))):
            x = random.randrange(0, l)
            y = random.randrange(0, l)
            copy[x], copy[y] = copy[y], copy[x]
        return "".join(copy)