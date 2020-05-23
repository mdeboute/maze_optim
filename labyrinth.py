import csv

class Labyrinth2D:
    """
    Class to store a 2D Labyrinth by specifying a truth value for each possible wall

    Attributes:
      n and m are the labyrinth dimension
      verticalWalls: n-1 x m array
        verticalWalls[i][j] is True iff there is a wall between (i, j) and (i+1, j)
      horizontalWalls: n x m-1 array
        horizontalWalls[i][j] is True iff there is a wall between (i, j) and (i, j+1)
    """

    def __init__(self, n, m):
        """Create a new labyrinth with all walls present"""

        self.n = n
        self.m = m
        self.verticalWalls = [ [True] * self.m for i in range(self.n-1) ]
        self.horizontalWalls = [ [True] * (self.m-1) for i in range(self.n) ]

    def saveCSV(self, file):
        """Save the labyrinth to file in CSV format"""

        writer = csv.writer(file, delimiter=' ')
        writer.writerow((self.n, self.m))
        for i in range(self.n - 1):
            for j in range(self.m):
                if self.verticalWalls[i][j]: writer.writerow((i, j, 'V'))
        for i in range(self.n):
            for j in range(self.m-1):
                if self.horizontalWalls[i][j]: writer.writerow((i, j, 'H'))

    def neighbors(self, pos):
        """Return the list of neighboring cells of position pos"""

        i, j = pos
        result = []
        if i > 0:
            if not self.verticalWalls[i-1][j]: result.append((i-1, j))
        if j > 0:
            if not self.horizontalWalls[i][j-1]: result.append((i, j-1))
        if i < self.n-1:
            if not self.verticalWalls[i][j]: result.append((i+1, j))
        if j < self.m-1:
            if not self.horizontalWalls[i][j]: result.append((i, j+1))
        assert result, "Empty neighbor list for position {p}".format(self.currentPosition)
        return result


    def printCompact(self):
        """Print the labyrinth as text, compact form"""

        table = { (True, True, True, True) : '┼',
                  (True, True, True, False) : '┴',
                  (True, True, False, True) : '┤',
                  (True, True, False, False) : '┘',
                  (True, False, True, True) : '┬',
                  (True, False, True, False) : '─',
                  (True, False, False, True) : '┐',
                  (True, False, False, False) : '╴',
                  (False, True, True, True) : '├',
                  (False, True, True, False) : '└',
                  (False, True, False, True) : '│',
                  (False, True, False, False) : '╵',
                  (False, False, True, True) : '┌',
                  (False, False, True, False) : '╶',
                  (False, False, False, True) : '╷',
                  (False, False, False, False) : ' '
                  }
        # Specific logic to include walls around the labyrinth
        def isVertWall(i, j):
            if i >= 0 and j >= 0 and i < self.n - 1 and j < self.m:
                return self.verticalWalls[i][j]
            return (i == -1 or i == self.n-1) and (j>= 0 and j < self.m)
        def isHorizWall(i, j):
            if i >= 0 and j >= 0 and i < self.n  and j < self.m - 1:
                return self.horizontalWalls[i][j]
            return (j == -1 or j == self.m-1) and (i>= 0 and i < self.n)

        def getWalls(i, j):
            return (isHorizWall(i-1, j-1),
                    isVertWall(i-1, j-1),
                    isHorizWall(i, j-1),
                    isVertWall(i-1, j))

        for j in range(self.m + 1):
            print("".join(table[getWalls(i, j)] for i in range(self.n + 1)))

    def printWide(self):
        """Print the labyrinth as text, wider form"""

        wallChar = '█'
        noWallChar = ' '
        cellChar = ' '
        def printLine(j):
            print(cellChar.join(wallChar if i == 0 or i == self.n or self.verticalWalls[i-1][j] else noWallChar
                                for i in range(self.n+1)))

        print(wallChar * (2*self.n + 1))
        for j in range(self.m-1):
            printLine(j)
            print(wallChar + wallChar.join(wallChar if self.horizontalWalls[i][j] else noWallChar
                                           for i in range(self.n)) + wallChar)
        printLine(self.m - 1)
        print(wallChar * (2*self.n + 1))


    def draw(self, filename, path = None, cell_size = 40, margin = 10):

        try:
            from wand.color import Color
            from wand.image import Image
            from wand.drawing import Drawing
            from wand.compat import nested
        except ImportError:
            print("Drawing labyrinths requires the wand package, see http://docs.wand-py.org/")
            exit(1)

        def top_left(i, j):
            return (margin + i * cell_size, margin + j * cell_size)
        def center(p):
            i, j = p
            half_cell = cell_size // 2
            return (margin + i * cell_size + half_cell, margin + j * cell_size + half_cell)

        def line(draw, p1, p2):
            old_fill = draw.fill_color
            draw.fill_color = draw.stroke_color
            xcoords = (p1[0], p2[0])
            ycoords = (p1[1], p2[1])
            draw.rectangle(left=min(xcoords) - 1, top=min(ycoords)-1,
                           right=max(xcoords) + 1, bottom=max(ycoords)+1)
            draw.fill_color = old_fill

        with Drawing() as draw:
            with Image(width=2*margin + cell_size * self.n, height = 2*margin + cell_size * self.m,
                       background=Color('white')) as img:
                draw.stroke_color = Color('black')
                draw.fill_color = Color('white')
                pos = top_left(0, 0)
                for p in ( top_left(0, self.m), top_left(self.n, self.m), top_left(self.n, 0), top_left(0, 0) ):
                    line(draw, pos, p)
                    pos = p
                # draw.fill_color = draw.stroke_color
                for i in range(self.n-1):
                    for j in range(self.m):
                        if self.verticalWalls[i][j]:
                            line(draw, top_left(i+1, j), top_left(i+1, j+1))
                for i in range(self.n):
                    for j in range(self.m-1):
                        if self.horizontalWalls[i][j]:
                            line(draw, top_left(i, j+1), top_left(i+1, j+1))

                if path:
                    draw.stroke_color = Color('red')
                    pos = (0, 0)
                    for p in path:
                        line(draw, center(pos), center(p))
                        pos = p

                draw(img)
                img.save(filename=filename)


class Labyrinth2DFromFile(Labyrinth2D):
    """Labyrinth class created by reading from a file in CSV format"""

    def __init__(self, file):
        """
        Create the labyrinth by reading from 'file'

        Raise ValueError if the file does not respect the format
        """
        reader = csv.reader(file, delimiter = ' ')
        try:
            rowSize = next(reader)
            line = 1
            if len(rowSize) != 2:
                raise ValueError('First Line should have length 2, not {}'.format(len(rowSize)))
            self.n = int(rowSize[0])
            self.m = int(rowSize[1])
            self.verticalWalls = [ [False] * self.m for i in range(self.n-1) ]
            self.horizontalWalls = [ [False] * (self.m-1) for i in range(self.n) ]
            for row in reader:
                line += 1
                if len(row) != 3:
                    raise ValueError('Lines after the first should have length 3, not {}'.format(len(rowSize)))
                i = int(row[0])
                j = int(row[1])
                t = row[2]
                if t == 'V':
                    if i >= 0 and i < self.n-1 and j >= 0 and j < self.m:
                        self.verticalWalls[i][j] = True
                    else:
                        raise ValueError('Position {}, {} is not valid for a vertical wall'.format(i, j))
                elif t == 'H':
                    if i >= 0 and i < self.n and j >= 0 and j < self.m-1:
                        self.horizontalWalls[i][j] = True
                    else:
                        raise ValueError('Position {}, {} is not valid for a horizontal wall'.format(i, j))
                else:
                    raise ValueError('Type {} is not valid, only V and H allowed'.format(t))
        except ValueError as e:
            raise ValueError("Line {}, error: {}".format(line, e))
