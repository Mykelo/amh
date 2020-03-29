import random
import math
import time
import sys
from copy import deepcopy
from map import *
from path import *

class TabuSearch:
    def __init__(self, tabulen, path):
        self.tabulen = tabulen
        self.tabu = []
        self.path = path

    def search(self, t, n):
        random.seed()
        timeout = time.time() + t

        # Generate path, calculate its cost and remember as the best path
        currPath = self.path.initPath()
        bestcost, best = self.path.cost(currPath)
        while timeout > time.time():
            # Tweak the current path and calculate cost
            currPath = self.path.tweak(currPath)
            newcost, currPath = self.path.cost(currPath)

            # Generate n neighbours of the current path and try to find a better solution
            for _ in range(n):
                if timeout <= time.time():
                    break
                
                neighbour = self.path.tweak(currPath)
                neigbourcost, neighbour = path.cost(neighbour)

                if neighbour not in self.tabu and neigbourcost < newcost:
                    newcost = neigbourcost
                    currPath = neighbour
                    self.tabu.append(currPath)

                # Control the length of the tabu list
                if len(self.tabu) > self.tabulen:
                    self.tabu = self.tabu[1:]
            if newcost < bestcost:
                bestcost = newcost
                best = currPath

        return best

t, n, m = (int(x) for x in input().split(" "))
labyrinth = [list(map(lambda x: int(x), input())) for _ in range(n)]
lab = Map(labyrinth)
path = NaivePathV2(lab)
tabusearch = TabuSearch(n, path)
path = tabusearch.search(t, 100)
print(len(path))
print(path, file=sys.stderr)