class Map:
    def __init__(self, m):
        self.map = m
        self.height = len(m)
        self.width = len(m[0])
        self.moves = {"U": (-1, 0), "L": (0, -1), "D": (1, 0), "R": (0, 1)}

    def __copy__(self):
        return type(self)([[x for x in row] for row in self.map])

    def __getitem__(self, key):
        return self.map[key]

    # Check if any of the neighbours is the exit and return its direction
    def checkExit(self, pos):
        neighbours = [(((pos[0] + v[0]) % self.height, (pos[1] + v[1]) % self.width), k) for k, v in self.moves.items()]
        res = [k for p, k in neighbours if self.map[p[0]][p[1]] == 8]
        if len(res) > 0:
            return True, res[0]
        return False, None

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