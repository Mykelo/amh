class Map:
    def __init__(self, m):
        self.map = m
        self.height = len(m)
        self.width = len(m[0])
        self.moves = {"U": (-1, 0), "L": (0, -1), "D": (1, 0), "R": (0, 1)}

    def checkExit(self, pos):
        neighbours = [((pos[0] + x) % self.height, (pos[1] + y) % self.width) for x, y in self.moves.values()]
        return any(self.map[n[0]][n[1]] == 8 for n in neighbours)

    def findStart(self):
        for x, row in enumerate(self.map):
            for y, _ in enumerate(row):
                if self.map[x][y] == 5:
                    return (x, y)
        return (-1, -1)

    def getDirection(self, move):
        return self.moves[move]

    def listDirections(self):
        return list(self.moves.keys())