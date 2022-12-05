class Node:
    def __init__(self, data: int, coordinate: tuple, lengthOfGrid: int) -> None:
        self.data = data
        self.gridSize = lengthOfGrid
        self.coordinate = coordinate
        self.neighbors = []
        # self.setNeighborsConstraint()

    def setNeighborsConstraint(self):
        """
        Assign the neighbors of a node in a grid.
        """
        # rowNeighborConstraints = self.getRowNeighbors()
        columnNeighborConstraint = self.getColumnNeighbors()
        diagonalNeighborConstraint = self.getDiagonalNeighbors()
        finalNeighborsConstraint = columnNeighborConstraint + diagonalNeighborConstraint

        # Assign the neighbors to the node attribute.
        self.neighbors.extend(finalNeighborsConstraint)

    def getRowNeighbors(self):
        """
        Get all the row neighbors of a node in a grid.
        """

        rowNeighborConstraints = []
        for i in range(1):
            for j in range(self.gridSize):
                if (self.coordinate[0], j) != self.coordinate:
                    rowNeighborConstraints.append(
                        [self.coordinate, (self.coordinate[0], j)]
                    )
        return rowNeighborConstraints

    def getColumnNeighbors(self):
        """
        Get all the column neighbors of a node in a grid.
        """

        columnNeighborConstraint = []
        for i in range(self.gridSize):
            for j in range(1):
                if (i, self.coordinate[1]) != self.coordinate:
                    columnNeighborConstraint.append(
                        [self.coordinate, (i, self.coordinate[1])]
                    )
        return columnNeighborConstraint

    def getDiagonalNeighbors(self):
        """
        Get all the diagonal neighbors of a node in a grid.
        """

        diagonalNeighborConstraint = []
        # Top left to bottom right diagonal
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if (i, j) != self.coordinate:
                    if (i - self.coordinate[0]) == (j - self.coordinate[1]) or (
                        i - self.coordinate[0]
                    ) == -(j - self.coordinate[1]):
                        diagonalNeighborConstraint.append([self.coordinate, (i, j)])

        return diagonalNeighborConstraint
