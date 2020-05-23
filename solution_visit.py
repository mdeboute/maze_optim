import random

def noMemoryVisit(choiceFunction, visit):
    previous = None
    step = 0
    while not visit.isFinish():
        neighbors = visit.currentNeighbors()
        nextPosition = choiceFunction(neighbors, previous)
        previous = visit.currentPosition
        visit.moveTo(nextPosition)
    return visit.visitLength

def randomChoiceFunction(neighbors, previous):
    if not previous:
        return random.choice(neighbors)
    idx = neighbors.index(previous)
    if len(neighbors) == 1: return neighbors[0]
    else: return random.choice(neighbors[:idx] + neighbors[idx+1:])

def leftHandVisitFunction(neighbors, previous):
    if not previous:
        return neighbors[0]
    idx = neighbors.index(previous)
    return neighbors[(idx + 1) % len(neighbors)]
    
def rightHandVisitFunction(neighbors, previous):
    if not previous:
        return neighbors[-1]
    idx = neighbors.index(previous)
    return neighbors[(idx - 1) % len(neighbors)]

def indexOfFirstPredicate(list, pred):
    for idx, x in enumerate(list):
        if pred(x): return idx
    raise ValueError("No element satisfies pred")


# Only works for non-cyclic (perfect) labyrinths,
# And only if the starting point is (0, 0)
def planarVisit(visit):

    def isVisited(p):
        return visit.visited[p[0]][p[1]]
    def isBorder(p):
        return p[0] == 0 or p[0] == visit.n - 1 or p[1] == 0 or p[1] == visit.m - 1

    
    assert visit.currentPosition == (0, 0)
    finished = { (i, j): False for i in range(visit.n) for j in range(visit.m) }
    previous = None
    step = 0
    while not visit.isFinish():
        neighbors = visit.currentNeighbors()
        if not previous: nextPosition = neighbors[0]
        else:
            if len(neighbors) == 1:
                nextPosition = neighbors[0]
                finished[visit.currentPosition] = True
            else:
                possibleChoices = list(filter(lambda p: not isVisited(p), neighbors))
                if not possibleChoices: 
                    finished[visit.currentPosition] = True
                    indexOfNext = indexOfFirstPredicate(neighbors, lambda p: not finished[p])
                    nextPosition = neighbors[indexOfNext]
                else:
                    nextPosition = random.choice(possibleChoices)
                            

        previous = visit.currentPosition
        visit.moveTo(nextPosition)
        if isBorder(nextPosition):
            if nextPosition[0] == 0:
                for j in range(nextPosition[1]):
                    i = 0
                    while not visit.visited[i][j]:
                        visit.visited[i][j] = True
                        finished[(i, j)] = True
                        i += 1
            elif nextPosition[0] == visit.n - 1:
                for j in range(nextPosition[1]):
                    i = visit.n - 1
                    while not visit.visited[i][j]:
                        visit.visited[i][j] = True
                        finished[(i, j)] = True
                        i -= 1
            elif nextPosition[1] == 0:
                for i in range(nextPosition[0]):
                    j = 0
                    while not visit.visited[i][j]:
                        visit.visited[i][j] = True
                        finished[(i, j)] = True
                        j += 1
            elif nextPosition[1] == visit.m - 1:
                for i in range(nextPosition[0]):
                    j = visit.m - 1
                    while not visit.visited[i][j]:
                        visit.visited[i][j] = True
                        finished[(i, j)] = True
                        j -= 1
    return visit.visitLength


# From https://en.wikipedia.org/wiki/Maze_solving_algorithm#cite_ref-10
# Source: Fattah, Mohammad; et, al. (2015-09-28). "A Low-Overhead,
# Fully-Distributed, Guaranteed-Delivery Routing Algorithm for 
# Faulty Network-on-Chips".
# NOCS '15 Proceedings of the 9th International Symposium on
# Networks-on-Chip. doi:10.1145/2786572.2786591.

def manhattanVisit(visit):
    def manhattanDistance(a, b): 
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    def distance(pos):
        return manhattanDistance(visit.target, pos)
    def direction(neighbor): # 0 for South, 1 for West, 2 for North, 3 for East
        p = visit.currentPosition
        if p[0] == neighbor[0] + 1: return 1
        elif p[0] == neighbor[0] - 1: return 3
        elif p[1] == neighbor[1] + 1: return 0
        else:
            assert p[1] == neighbor[1] -1
            return 2

    bestSoFar = distance(visit.currentPosition)
    goingLeftHand = False
    previous = None
    while not visit.isFinish():
        neighbors = visit.currentNeighbors()
        currentDistance = distance(visit.currentPosition)
        productive = False
        if bestSoFar == currentDistance:
            try:
                idx = indexOfFirstPredicate(neighbors, lambda p: distance(p) < currentDistance)
                goingLeftHand = False
                nextPosition = neighbors[idx]
                bestSoFar -= 1
                productive = True
            except ValueError: pass
        if not productive: 
            if goingLeftHand:
                nextPosition = leftHandVisitFunction(neighbors, previous)
            else: 
                nextPosition = max(neighbors, key = direction)
                goingLeftHand = True

        previous = visit.currentPosition
        visit.moveTo(nextPosition)

    return visit.visitLength

        
if __name__ == "__main__":
    import argparse
    from labyrinth import *
    from visit import *

    parser = argparse.ArgumentParser("Visit a labyrinth with several algorithms")
    parser.add_argument("file", type = argparse.FileType('r'), help = "input file")
    parser.add_argument("type", choices = ("random", "right", "left", "planar", "manh"), help = "visit type")
    parser.add_argument("-q", dest = "display", action = "store_false",
                        help = "Turn off displaying")
    parser.add_argument("-d", dest = "delay", type = float, default = 0.05,
                        help = "Time delay between two displays")
    parser.add_argument("-i", dest = "interval", type = int, default = 1,
                        help = "Number of step between two displays")
    parser.add_argument("-n", dest = "repet", type = int, default = 1,
                        help = "Number of repetitions of the algorithm")
    
    args = parser.parse_args()
    lab = Labyrinth2DFromFile(args.file)
    if args.type == "planar":
        sum = 0
        for _ in range(args.repet):
            visit = Visit(lab, args.display, sleepTime = args.delay, displayFrequency = args.interval)
            sum += planarVisit(visit)
        print("Average: {}".format(sum / args.repet))
    elif args.type == "manh":
        visit = Visit(lab, args.display, sleepTime = args.delay, displayFrequency = args.interval)
        manhattanVisit(visit)
    else: 
        if args.type == "random":
            fun = randomChoiceFunction
        elif args.type == "right":
            fun = rightHandVisitFunction
        elif args.type == "left":
            fun = leftHandVisitFunction

        sum = 0
        for _ in range(args.repet):
            visit = Visit(lab, args.display, sleepTime = args.delay, displayFrequency = args.interval)
            sum += noMemoryVisit(fun, visit)
        print("Average: {}".format(sum / args.repet))

def rightHandVisit(visit):
    return noMemoryVisit(rightHandVisitFunction, visit)

def leftHandVisit(visit):
    return noMemoryVisit(leftHandVisitFunction, visit)

def randomVisit(visit):
    return noMemoryVisit(randomChoiceFunction, visit)
