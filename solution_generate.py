import labyrinth
import random

class Components:
    def __init__(self, values):
        self.dict = { x:None for x in values }

    def getRepresentative(self, x):
        y = self.dict[x]
        encountered = [x]
        while y is not None:
            encountered.append(y)
            y = self.dict[y]
        result = encountered[-1]
        for z in encountered[:-1]:
            self.dict[z] = result
        return result

    def connect(self, x, y):
        rx = self.getRepresentative(x)
        ry = self.getRepresentative(y)
        assert rx != ry
        assert self.dict[rx] is None
        self.dict[rx] = ry

    def areConnected(self, x, y):
        rx = self.getRepresentative(x)
        ry = self.getRepresentative(y)
        return rx == ry

    def connectIfPossible(self, x, y):
        rx = self.getRepresentative(x)
        ry = self.getRepresentative(y)
        if rx == ry:
            return False
        self.dict[rx] = ry
        return True

class SlowComponents(Components):
    def __init__(self, values):
        super().__init__(values)
        
    def getRepresentative(self, x):
        y = self.dict[x]
        while y is not None:
            x = y
            y = self.dict[y]
        return x
    
    

class GenerateLabyrinth2D(labyrinth.Labyrinth2D):
    def __init__(self, n, m, slow = False):
        self.n = n
        self.m = m
        self.verticalWalls = [ [True] * m for i in range(n-1) ]
           # verticalWalls[i][j] is True iff there is a wall between (i, j) and (i+1, j)
        self.horizontalWalls = [ [True] * (m-1) for i in range(n) ]
           # horizontalWalls[i][j] is True iff there is a wall between (i, j) and (i, j+1)


        nodes = self.allNodes()
        edges = self.possibleEdges()

        # def select(e):
        #     return (e[2] and e[0] < n/2) or (not e[2] and e[0]>= n/2)
        # def split(data, pred=bool):
        #     yes, no = [], []
        #     for d in data:
        #         if pred(d): yes.append(d)
        #         else: no.append(d)
        #     return (yes, no)
        # part1, part2 = split(edges, select)
        # random.shuffle(part1)
        # random.shuffle(part2)
        # edges = part1 + part2
        random.shuffle(edges)
        
        if slow:
            comp = SlowComponents(nodes)
        else: 
            comp = Components(nodes)
        nbComps = len(nodes)
        for e in edges:
            (i, j, isVertical) = e
            if isVertical: dest = (i+1, j)
            else: dest = (i, j+1)
            if comp.connectIfPossible((i, j), dest):
                nbComps -= 1
                self.removeWall(i, j, isVertical)
                if nbComps == 1: break
           

    # List of possible edges as (i, j, isVertical)
    def possibleEdges(self):
        return ( [ (i, j, True) for i in range(self.n-1) for j in range(self.m) ]
                 + [ (i, j, False) for i in range(self.n) for j in range(self.m-1) ] )

    def allNodes(self):
        return [ (i, j) for i in range(self.n) for j in range(self.m) ]

    def removeWall(self, i, j, isVertical):
        if isVertical: 
            self.verticalWalls[i][j] = False
        else: 
            self.horizontalWalls[i][j] = False


    def removeRandomWalls(self, nb):
        found = 0
        while found < nb:
            if random.getrandbits(1):
                i = random.randrange(self.n - 1)
                j = random.randrange(self.m)
                if self.verticalWalls[i][j]:
                    self.verticalWalls[i][j] = False
                    found += 1
            else: 
                i = random.randrange(self.n)
                j = random.randrange(self.m - 1)
                if self.horizontalWalls[i][j]:
                    self.horizontalWalls[i][j] = False
                    found += 1
    

            
if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser("Generate a labyrinth of given size")
    parser.add_argument("n", type = int, help = "Number of columns of the labyrinth")
    parser.add_argument("m", type = int, help = "Number of rows of the labyrinth")
    parser.add_argument("-o", dest = "file", type = argparse.FileType('w'),
                        help = "File to save the result", default = sys.stdout)
    parser.add_argument("--slow", action = "store_true",
                        help = "Use the slow algorithm for checking connected components")
    parser.add_argument("-s", "--show", action = "store_true",
                        help = "Show the result in compact form")
    parser.add_argument("-d", "--draw", default = None,
                        help = "Draw the result in an image with this filename")
    parser.add_argument("-r", dest = "random", metavar = "X", type = int, default = 0,
                        help = "Remove X random walls from the labyrinth")

    args = parser.parse_args()
    
    lab = GenerateLabyrinth2D(args.n, args.m, slow = args.slow)
    if args.random:
        lab.removeRandomWalls(args.random)
    if args.show:
        lab.printCompact()
    if args.draw:
        lab.draw(args.draw)
    lab.saveCSV(args.file)
