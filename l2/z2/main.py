import time
import math
import functools
import sys
import random

class Matrix:
    def __init__(self):
        self.m = []
        self.blocks = []
        self.possibleValues = [0, 32, 64, 128, 160, 192, 223, 255]
        self.k = 0

    def fill(self, n, m, k):
        nBlocks = [k] * (n // k)
        mBlocks = [k] * (m // k)

        for _ in range(n % k):
            nBlocks[random.randrange(len(nBlocks))] += 1

        for _ in range(m % k):
            mBlocks[random.randrange(len(mBlocks))] += 1

        matrix = [[0] * m for _ in range(n)]
        curri = 0
        for nBlock in nBlocks:
            currj = 0
            for mBlock in mBlocks:
                value = random.choice(self.possibleValues)
                for i in range(curri, curri + nBlock):
                    for j in range(currj, currj + mBlock):
                        matrix[i][j] = value
                currj += mBlock
            curri += nBlock
        self.m = matrix
        self.blocks = [[[x, y] for y in mBlocks] for x in nBlocks]
        self.k = k

    def fillBlock(self, matrix, x, y, value):
        xMatrixIndex, yMatrixIndex = self.getBlockIndices(x, y)

        for i in range(xMatrixIndex, xMatrixIndex + self.blocks[x][y][0]):
            for j in range(yMatrixIndex, yMatrixIndex + self.blocks[x][y][1]):
                matrix[i][j] = value
        return matrix

    def randomValueChange(self):
        x = random.randrange(len(self.blocks))
        y = random.randrange(len(self.blocks[0]))
        newValue = random.choice(self.possibleValues)

        newM = [[v for v in row] for row in self.m]
        newM = self.fillBlock(newM, x, y, newValue)

        return newM

    def getBlockIndices(self, xBlock, yBlock):
        xMatrixIndex = sum([self.blocks[i][yBlock][0] for i in range(xBlock)])
        yMatrixIndex = sum([self.blocks[xBlock][i][1] for i in range(yBlock)])
        return xMatrixIndex, yMatrixIndex

    def swapBlocks(self):
        if len(self.blocks) <= 1 and len(self.blocks[0]) <= 1:
            return

        # Make sure that chosen blocks are not the same block
        x1, x2 = random.choices(range(len(self.blocks)), k=2)
        if x1 == x2:
            y1, y2 = random.sample(range(len(self.blocks[0])), 2)
        else:
            y1, y2 = random.choices(range(len(self.blocks[0])), k=2)

        b1 = self.blocks[x1][y1]
        b2 = self.blocks[x2][y2]
        nDiff = b1[0] - b2[0]
        mDiff = b1[1] - b2[1]
        x1MatrixIndex, y1MatrixIndex = self.getBlockIndices(x1, y1)
        x2MatrixIndex, y2MatrixIndex = self.getBlockIndices(x2, y2)
        b1Value = self.m[x1MatrixIndex][y1MatrixIndex]
        b2Value = self.m[x2MatrixIndex][y2MatrixIndex]

        def correctSizes(bigger, diff, x, y, direction):
            isCol = 1 if direction == 'col' else 0
            isRow = 1 if direction == 'row' else 0

            border0Condition = x - 1 >= 0 if direction == 'col' else y - 1 >= 0
            borderMaxCondition = x + 1 < len(self.blocks) if direction == 'col' else y + 1 < len(self.blocks[0])

            # Check neighbours of the smaller block in this direction
            # If any of the neighbours will be bigger than k, cut it
            if border0Condition and self.blocks[x - isCol][y - isRow][isRow] + diff >= self.k:
                self.blocks[x - isCol][y - isRow][isRow] += diff
            elif borderMaxCondition and self.blocks[x + isCol][y + isRow][isRow] + diff >= self.k:
                self.blocks[x + isCol][y + isRow][isRow] += diff
            else:
                bigger[isRow] += diff

            return bigger

        if nDiff != 0:
            if nDiff < 0:
                b1[0] = b2[0]
                b2 = correctSizes(b2, nDiff, x1, y1, 'col')
            else:
                b2[0] = b1[0]
                b1 = correctSizes(b1, (-1) * nDiff, x2, y2, 'col')
        
        if mDiff != 0:
            if mDiff < 0:
                b1[1] = b2[1]
                b2 = correctSizes(b2, mDiff, x1, y1, 'row')
            else:
                b2[1] = b1[1]
                b1 = correctSizes(b1, (-1) * mDiff, x2, y2, 'row')

        self.blocks[x1][y1], self.blocks[x2][y2] = self.blocks[x2][y2], self.blocks[x1][y1]
        newM = [[v for v in row] for row in self.m]
        newM = self.fillBlock(newM, x1, y1, b2Value)
        newM = self.fillBlock(newM, x2, y2, b1Value)
        return newM

    def tweak(self):
        tweaked = Matrix()
        tweaked.k = self.k
        tweaked.m = self.randomValueChange() if random.random() < 0.5 else self.swapBlocks()
        tweaked.blocks = self.blocks
        return tweaked


def distance(matrix1, matrix2):
    m1 = matrix1.m
    m2 = matrix2.m
    dist = 0
    for i in range(len(m1)):
        for j in range(len(m1[0])):
            dist += (m1[i][j] - m2[i][j]) ** 2
    return dist


def simAnnealing(maxTime, t, c, initSolution, f):
    timeout = time.time() + maxTime
    s = initSolution
    best = initSolution
    while timeout > time.time() and t > 0:
        r = s.tweak()
        if f(r) < f(s) or random.random() < math.exp((f(s) - f(r)) / t):
            s = r
        t = t * c
        if f(s) < f(best):
            best = s
    return best


params = input().strip().split(" ")
t = int(params[0])
n = int(params[1])
m = int(params[2])
k = int(params[3])

M = Matrix()
for _ in range(n):
    M.m.append([int(x) for x in input().strip().split(" ")])

initSolution = Matrix()
initSolution.fill(n, m, k)

print(distance(initSolution, M))
solution = simAnnealing(t, 100, 0.997, initSolution, lambda x: distance(x, M))
print(distance(solution, M))
