# from labyrinth import *
import io
import os
import time


class Visit:
    """
    Describe a visit in a labyrinth

    Attributes: 
      currentPosition: tuple (i, j) describing the cell currently being visited
      target:          tuple describing the exit's coordinates
      visitLength:     number of steps so far
      visited:         n x m boolean array, True for all visited cells
    """

    
    def __init__(self, laby, display = False, sleepTime = 0.05, displayFrequency = 1):
        """
        Start a new visit
        
        Parameters: 
          laby:             a Labyrinth2D object to visit
          display:          show the visit in the terminal
          sleepTime:        time to wait between two displays
          displayFrequency: number of steps between two displays

        """
        self.labyrinth = laby
        self.n = self.labyrinth.n
        self.m = self.labyrinth.m
        self.currentPosition = (0, 0)
        self.visited = [ [False] * self.m for i in range(self.n) ]
        self.visitCurrent()
        self.target = (self.n - 1, self.m - 1)
        self.visitLength = 1

        self.display = display
        if self.display:
            self.step = 0
            self.sleepTime = sleepTime
            self.displayFrequency = displayFrequency
            os.system('clear')
            self.printWideVisited()

    def visitCurrent(self):
        i, j = self.currentPosition
        self.visited[i][j] = True
        
    def currentNeighbors(self):
        return self.labyrinth.neighbors(self.currentPosition)
        
    def isFinish(self):
        """
        Return True if the visit is at the target

        Also display the total length if the visit is finished
        """
        finish = self.currentPosition == self.target
        if finish:
            if self.display:
                os.system('clear')
                self.printWideVisited()
            print("Total visit length:", self.visitLength)
        return finish

    def moveTo(self, nextPosition):
        """
        Move to a new position

        nextPosition should belong to the list returned by currentNeighbors()
        """
        def getError(s, t):
            (i, j) = s
            (u, v) = t
            if u == i+1:
                if v != j:
                    return "Invalid move"
                if self.labyrinth.verticalWalls[i][j]:
                    return "Wall exists"
            elif v == j+1:
                if i != u:
                    return "Invalid move"
                if self.labyrinth.horizontalWalls[i][j]:
                    return "Wall exists"
            elif u == i-1 or v == j-1:
                return getError(t, s)
            else:
                return "Invalid move"
            return None
        errorMessage = getError(self.currentPosition, nextPosition)
        if errorMessage:
            raise ValueError("From {} to {}: {}".format(self.currentPosition, nextPosition, errorMessage))
        self.currentPosition = nextPosition
        self.visitCurrent()
        self.visitLength += 1
        if self.display:
            self.step += 1
            if self.step == self.displayFrequency:
                self.step = 0
                time.sleep(self.sleepTime)
                os.system('clear')
                self.printWideVisited()

        
    def printWideVisited(self):
        """
        Print the current state of the visit
        
        Differentiate between current cell, visited cells, and other empty cells.
        """
        wallChar = '█'
        noWallChar = ' '
        emptyCellChar = ' '
        visitedCellChar = '‧'
        currentCellChar = '◇'
        def printLine(j):
            buf = io.StringIO()
            buf.write(wallChar)
            for i in range(self.n):
                if (i, j) == self.currentPosition: buf.write(currentCellChar)
                elif self.visited[i][j]: buf.write(visitedCellChar)
                else: buf.write(emptyCellChar)
                if i < self.n-1:
                    if self.labyrinth.verticalWalls[i][j]: buf.write(wallChar)
                    else: buf.write(noWallChar)
            buf.write(wallChar)
            print(buf.getvalue())
            buf.close()

        print(wallChar * (2*self.n + 1))
        for j in range(self.m-1):
            printLine(j)
            print(wallChar + wallChar.join(wallChar if self.labyrinth.horizontalWalls[i][j] else noWallChar
                                           for i in range(self.n)) + wallChar)
        printLine(self.m - 1)
        print(wallChar * (2*self.n + 1))
