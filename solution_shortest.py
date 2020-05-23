
def shortestPath(lab):
    startingPoint = (0, 0)
    target = (lab.n - 1, lab.m - 1)
    distances = { (i,j): None for i in range(lab.n) for j in range(lab.m) }
    candidates = [startingPoint]
    distances[startingPoint] = (0, None)
    lastDistance = 0
    isPerfect = True
    while candidates:
        p = candidates.pop(0)
        d, _ = distances[p]
        assert d in [lastDistance, lastDistance+1]
        lastDistance = d
        for q in lab.neighbors(p):
            if not distances[q]:
                distances[q] = (d + 1, p)
                candidates.append(q)
                if q == target:
                    break
            elif distances[q][0] != d-1:
                isPerfect = False
    path = []
    current = target
    while current != startingPoint:
        path.append(current)
        _, current = distances[current]
    path = list(reversed(path))

    return path, isPerfect


if __name__ == "__main__":
    from labyrinth import *
    from visit import Visit
    import argparse

    parser = argparse.ArgumentParser("Visit a labyrinth with shortest path")
    parser.add_argument("file", type = argparse.FileType('r'), help = "input file")
    parser.add_argument("-q", dest = "display", action = "store_false",
                        help = "Turn off displaying")
    parser.add_argument("-d", dest = "delay", type = float, default = 0.05,
                        help = "Time delay between two displays")
    parser.add_argument("-i", dest = "interval", type = int, default = 1,
                        help = "Number of step between two displays")
    parser.add_argument("--draw", default=None, help="Draw the labyrinth and the path in a file")
    
    args = parser.parse_args()
    lab = Labyrinth2DFromFile(args.file)
    path, isPerfect = shortestPath(lab)
    if not isPerfect: print("Imperfect labyrinth !")
    visit = Visit(lab, display = args.display, sleepTime = args.delay, displayFrequency = args.interval)
    for p in path:
        visit.moveTo(p)
    assert visit.isFinish()
    if args.draw:
        lab.draw(args.draw, path=path)
