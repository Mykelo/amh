import random
from copy import deepcopy, copy
import math


class Path:
    def __init__(self, m):
        self.map = m
        self.start = m.findStart()

    def initPath(self):
        return ""

    def move(self, pos, move, map):
        xdir, ydir = map.getDirection(move)
        newx, newy = (pos[0] + xdir, pos[1] + ydir)
        return (newx, newy) if map.map[newx][newy] == 0 or map.map[newx][newy] == 8 else pos

    def cost(self, path):
        return 0

    def tweak(self, path):
        return ""


class NaivePath(Path):
    # Follow the walls to find the exit
    def initPath(self):
        path = ""
        directionsOrder = ["U", "L", "D", "R"]
        currDir = 0
        pos = deepcopy(self.start)
        lastStep = self.map.checkExit(pos)
        mapCopy = copy(self.map)
        stack = []
        stack.append((self.move(pos, directionsOrder[currDir], mapCopy), pos, currDir + 3, 'R'))
        stack.append((self.move(pos, directionsOrder[currDir], mapCopy), pos, currDir + 2, 'D'))
        stack.append((self.move(pos, directionsOrder[currDir], mapCopy), pos, currDir + 1, 'L'))
        stack.append((self.move(pos, directionsOrder[currDir], mapCopy), pos, currDir, 'U'))
        while len(stack) > 0:
            currstep = stack.pop()
            newpos = currstep[0]
            lastStep = mapCopy.checkExit(newpos)
            if newpos != currstep[1] and lastStep[0]:
                path = currstep[3]
                # path += directionsOrder[currstep[2]]
                path += lastStep[1]
                return path
            if newpos != currstep[1]:
                mapCopy[newpos[0]][newpos[1]] = 2
                direction = currstep[2]
                # path += directionsOrder[direction]
                # newpathlen = currstep[3] + 1
                # print(directionsOrder[direction])
                stack.append((self.move(newpos, directionsOrder[(
                    direction + 3) % 4], mapCopy), 
                    newpos, 
                    (direction + 3) % 4, 
                    currstep[3] + directionsOrder[(direction + 3) % 4]))
                stack.append((self.move(newpos, directionsOrder[(
                    direction + 2) % 4], mapCopy), 
                    newpos, 
                    (direction + 2) % 4, 
                    currstep[3] + directionsOrder[(direction + 2) % 4]))
                stack.append((self.move(newpos, directionsOrder[(
                    direction + 1) % 4], mapCopy), 
                    newpos, 
                    (direction + 1) % 4, 
                    currstep[3] + directionsOrder[(direction + 1) % 4]))
                stack.append((self.move(newpos, directionsOrder[(
                    direction + 0) % 4], mapCopy), 
                    newpos, 
                    (direction + 0) % 4, 
                    currstep[3] + directionsOrder[(direction + 0) % 4]))
        print('found nothing')
        return path

    def cost(self, path):
        lastStep = self.map.checkExit(self.start)
        if lastStep[0] or len(path) == 0:
            return 0, lastStep[1]

        pos = deepcopy(self.start)
        cost = 1
        for step in path:
            newpos = self.move(pos, step, self.map)
            # print(newpos, self.map[newpos[0]][newpos[1]])
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
        # maxnum = max(int(l / 5), 2)
        # # Swap random number of random pairs
        # for _ in range(random.randrange(1, maxnum)):
        #     x = random.randrange(0, l)
        #     y = random.randrange(0, l)
        #     copy[x], copy[y] = copy[y], copy[x]

        directionsOrder = ["U", "L", "D", "R"]
        if random.random() < 0.4 and l > 0:
            # print('inversing')
            s1 = random.randrange(0, l)
            s2 = random.randrange(0, l - s1) + s1
            # print(path)
            copy = copy[:s1] + copy[s1:s2][::-1] + copy[s2:]
        elif random.random() < 0.15 and l > 0:
            # print('deleting')
            length = random.randint(0, min(l // 5, 5))
            index = random.randrange(0, l - length)
            # print(path)
            copy = copy[:index] + copy[index + length:]
        else:
            s1 = random.randrange(0, l)
            s2 = random.randrange(0, l - s1) + s1
            newFragment = [random.choice(directionsOrder) for _ in range(s2 - s1)]
            # print(path)
            copy = copy[:s1] + newFragment + copy[s2:]
        # else:
        #     # print('adding')
        #     length = random.randint(0, max(2, l // 2))
        #     newFragment = [random.choice(directionsOrder) for _ in range(length)]
        #     index = random.randrange(0, l) if l > 0 else 0
        #     # print(path)
        #     copy = copy[:index] + newFragment + copy[index:]
        # print("".join(copy))
        return "".join(copy)
