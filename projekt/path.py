import random
from copy import deepcopy, copy
import math


class Path:
    def __init__(self, m):
        self.map = m
        self.start = m.findStart()

    def move(self, pos, move, map):
        xdir, ydir = map.getDirection(move)
        newx, newy = (pos[0] + xdir, pos[1] + ydir)
        if map.map[pos[0]][pos[1]] == 2 and ydir != 0:
            return pos
        if map.map[pos[0]][pos[1]] == 3 and xdir != 0:
            return pos
        if map.map[newx][newy] == 2 and xdir != 0:
            return (newx, newy)
        if map.map[newx][newy] == 3 and ydir != 0:
            return (newx, newy)
        return (newx, newy) if map.map[newx][newy] == 0 or map.map[newx][newy] == 8 else pos

    def cost(self, path):
        lastStep = self.map.checkExit(self.start)
        if lastStep[0] or len(path) == 0:
            return 0, lastStep[1], [0, 0]

        pos = deepcopy(self.start)
        first_pos = deepcopy(self.start)
        cost = 1
        for step in path:
            newpos = self.move(pos, step, self.map)
            if newpos == pos:
                return math.inf, path[0:cost-1], (newpos[0] - first_pos[0], newpos[1] - first_pos[1])
            lastStep = self.map.checkExit(newpos)
            if lastStep[0]:
                return cost, path[0:cost] + (lastStep[1] if lastStep[1] else ""), (newpos[0] - first_pos[0], newpos[1] - first_pos[1])

            cost += 1
            pos = newpos
        return math.inf, path, (pos[0] - first_pos[0], pos[1] - first_pos[1])

    def initPath(self):
        path = ""
        directionsOrder = ["U", "L", "D", "R"]
        currDir = 0
        pos = deepcopy(self.start)
        lastStep = self.map.checkExit(pos)
        while not lastStep[0]:
            newpos = self.move(pos, directionsOrder[currDir], self.map)
            if newpos == pos:
                currDir = random.randint(0, 3)
            else:
                pos = newpos
                path += directionsOrder[currDir]
                if random.random() < 0.15:
                    currDir = random.randint(0, 3)

            if len(path) > self.map.width * self.map.height / 3:
                pos = deepcopy(self.start)
                path = ""
            lastStep = self.map.checkExit(pos)
        
        # Add the last step leading to the exit if the path reached it
        if lastStep[1]:
            path += lastStep[1]
        return path

    
    def tweak(self, path):
        copy = [x for x in path]
        l = len(copy)

        directionsOrder = ["U", "L", "D", "R"]
        r = random.random()
        if r < 0.1 and l > 0:
            s1 = random.randrange(0, l)
            s2 = random.randrange(0, l - s1) + s1
            copy = copy[:s1] + copy[s1:s2][::-1] + copy[s2:]
        elif r < 0.2 and l > 0:
            length = random.randint(0, min(l // 5, 5))
            index = random.randrange(0, l - length)
            copy = copy[:index] + copy[index + length:]
        elif r < 1:
            s1 = random.randrange(0, l)
            s2 = random.randrange(0, l - s1) + s1
            newFragment = [random.choice(directionsOrder) for _ in range(s2 - s1)]
            copy = copy[:s1] + newFragment + copy[s2:]

        return "".join(copy)
