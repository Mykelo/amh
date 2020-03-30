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
        lastStep = self.map.checkExit(pos)
        while not lastStep[0]:
            newpos = self.move(pos, directionsOrder[currDir])
            if newpos == pos:
                currDir = (currDir + 1) % 4
            else:
                pos = newpos
                path += directionsOrder[currDir]
            lastStep = self.map.checkExit(pos)
        
        # Add the last step leading to the exit if the path reached it
        if lastStep[1]:
            path += lastStep[1]
        return path

    def cost(self, path):
        lastStep = self.map.checkExit(self.start)
        if lastStep[0] or len(path) == 0: return 0, lastStep[1]

        pos = deepcopy(self.start)
        cost = 1
        for step in path:
            newpos = self.move(pos, step)
            if newpos == pos:
                return math.inf, path
            lastStep = self.map.checkExit(newpos)
            if lastStep[0]:
                return cost, path[0:cost] + (lastStep[1] if lastStep[1] else "")

            cost += 1
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
        maxnum = max(int(l / 5), 2)
        # Swap random number of random pairs
        for _ in range(random.randrange(1, maxnum)):
            x = random.randrange(0, l)
            y = random.randrange(0, l)
            copy[x], copy[y] = copy[y], copy[x]
        return "".join(copy)