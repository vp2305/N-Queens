# Select one conflicted queen and then choose the best move for that queen.

from random import randint
from copy import deepcopy


class Chess:
    def __init__(self, height, width, maxSteps) -> None:
        self.height = height
        self.width = width
        self.maxSteps = maxSteps
        self.numberOfQueens = height
        self.grid = []
        self.queens = []
        self.columnQueens = {}
        self.rightDiagonalQueens = {}
        self.leftDiagonalQueens = {}
        self.numberOfAttacks = -1
        self.createChessboard()
        self.updateColumnDiagonalQueens()
        self.getNumberOfAttacks()

    def createChessboard(self) -> None:
        """
        Create the chessboard and place queens.
        """
        columns = [i for i in range(self.width)]
        for i in range(self.height):
            self.grid.append([])
            randomColumnIdx = randint(0, len(columns) - 1)
            randomColumn = columns[randomColumnIdx]
            for j in range(self.width):
                if randomColumn == j:
                    self.grid[i].append(1)
                    self.queens.append((i, j))
                    columns.remove(columns[randomColumnIdx])
                else:
                    self.grid[i].append(0)

    def printChessboard(self) -> None:
        """
        Print the chessboard.
        """
        for i in range(self.height):
            print("|", end=" ")
            for j in range(self.width):
                print(self.grid[i][j], end=" ")
            print("|")
        print("Number of attacking queens: ", self.numberOfAttacks)

    def getNumberOfAttacks(self) -> None:
        """
        Number of attacks between queens.
        """

        # Reset the number of attacks.
        self.numberOfAttacks = 0

        for queen in self.queens:
            (row, column) = queen
            # get row conflict
            self.numberOfAttacks += self.columnQueens.get(column) - 1
            # get right diagonal conflict
            self.numberOfAttacks += self.rightDiagonalQueens.get(column - row) - 1
            # get left diagonal conflict
            self.numberOfAttacks += self.leftDiagonalQueens.get(row + column) - 1

        # Divide the number of attacks by 2 because each queen is counted twice.
        self.numberOfAttacks = self.numberOfAttacks // 2

    def updateColumnDiagonalQueens(self) -> None:
        """
        Update the column and diagonal queens.
        """
        for queen in self.queens:
            (row, column) = queen
            # Update the column queens.
            self.columnQueens[column] = self.columnQueens.get(column, 0) + 1
            # Add all the queens in the right diagonal.
            self.rightDiagonalQueens[column - row] = (
                self.rightDiagonalQueens.get((column - row), 0) + 1
            )
            # Add all the queens in the left diagonal.
            self.leftDiagonalQueens[row + column] = (
                self.leftDiagonalQueens.get((row + column), 0) + 1
            )

    def minConflict(self) -> bool:
        """
        Min conflicts algorithm uses csp and maximum steps to solve the problem.

        The initial state is can be chosen randomly or by a greedy algorithm that chooses a minimal-conflict value for each variable in turn.
        """
        for i in range(self.maxSteps):
            if self.solvedCheck():
                print(f"Chessboard solved in {i} steps.")
                # self.printChessboard()
                return True
            else:
                # Go and move each queen to the position that minimizes the number of conflicts and select a state with the least conflicts.
                print(f"Step {i}:")
                # print("Queens: ", self.queens)
                minimumConflict = (
                    {}
                )  # Key: Number of conflicts. Value: [(Queen), (New Position)],
                for queen in self.queens:
                    if (self.getQueenConflict(queen)) > 0:
                        newQueenPosition, newQueenConflict = self.conflicts(queen)
                        if newQueenConflict not in minimumConflict.keys():
                            minimumConflict[newQueenConflict] = []
                        minimumConflict[newQueenConflict].append(
                            (queen, newQueenPosition)
                        )

                # If there is no conflict, then the chessboard is solved.
                if len(minimumConflict) != 0:
                    # Select a state with the least conflicts.

                    # Sort the minimum conflict dictionary by the number of conflicts.
                    sortedMinimumConflict = sorted(
                        minimumConflict.items(), key=lambda x: x[0]
                    )

                    # Move the queen to the new position.
                    # Select a random state with the least conflicts.
                    (queen, newQueenPosition) = sortedMinimumConflict[0][1][
                        randint(0, len(sortedMinimumConflict[0][1]) - 1)
                    ]

                    self.moveQueen(queen, newQueenPosition)
                    # Update queen positions.
                    self.queens.remove(queen)
                    self.queens.append(newQueenPosition)

                # self.printChessboard()
        print(f"Chessboard not solved\nTry increasing max steps.")
        print(f"Number of queens: {len(self.queens)}")
        return False

    def conflicts(self, conflictedQueen: tuple):
        """
        Determine a move that will minimize the number of conflicts.
        """
        (row, column) = conflictedQueen
        minConflict = self.getQueenConflict(conflictedQueen)
        minConflictCoordinate = conflictedQueen
        for i in range(self.width):
            if i != column:
                self.moveQueen(conflictedQueen, (row, i))
                newQueenConflict = self.getQueenConflict((row, i))
                if newQueenConflict < minConflict:
                    minConflict = newQueenConflict
                    minConflictCoordinate = (row, i)
                elif newQueenConflict == minConflict:
                    if randint(0, 1) == 0:
                        minConflict = newQueenConflict
                        minConflictCoordinate = (row, i)
                # print("Here")
                self.moveQueen((row, i), conflictedQueen)
        return minConflictCoordinate, minConflict

    def moveQueen(self, queen: tuple, newPosition: tuple) -> None:
        """
        Move a queen to a new column.
        """
        (row, column) = queen
        (newRow, newColumn) = newPosition
        previousQueenConflict = self.getQueenConflict(queen)

        # Remove the queen from the column and diagonal queens.
        self.columnQueens[column] -= 1
        self.rightDiagonalQueens[column - row] -= 1
        self.leftDiagonalQueens[row + column] -= 1

        # Move the queen to the new column.
        self.grid[row][column] = 0
        self.grid[newRow][newColumn] = 1

        # Update the column and diagonal queens.
        self.columnQueens[newColumn] = self.columnQueens.get(newColumn, 0) + 1
        self.rightDiagonalQueens[newColumn - newRow] = (
            self.rightDiagonalQueens.get((newColumn - newRow), 0) + 1
        )
        self.leftDiagonalQueens[newRow + newColumn] = (
            self.leftDiagonalQueens.get((newRow + newColumn), 0) + 1
        )

        # Update the number of attacks.
        # print("Previous number of attacks: ", self.numberOfAttacks)
        newQueenConflict = self.getQueenConflict(newPosition)
        self.numberOfAttacks += newQueenConflict - previousQueenConflict
        # print("New number of attacks: ", self.numberOfAttacks)

    def getConflictedQueen(self) -> tuple:
        """
        Go through all the queens and find the queen with the most conflicts.
        """
        maxConflictQueen = {}
        for queen in self.queens:
            numberOfConflicts = self.getQueenConflict(queen)
            if numberOfConflicts > 0:
                if numberOfConflicts not in maxConflictQueen.keys():
                    maxConflictQueen[numberOfConflicts] = []
                maxConflictQueen[numberOfConflicts].append(queen)

        # Get the queen with the most conflicts.
        sortedConflictedQueen = sorted(
            maxConflictQueen.items(), key=lambda x: x[0], reverse=True
        )
        mostConflictedQueenList = sortedConflictedQueen[0][1]
        # Choose a random queen from the list of queens with the most conflicts.
        conflictedQueen = mostConflictedQueenList[
            randint(0, len(mostConflictedQueenList) - 1)
        ]
        return conflictedQueen

    def getQueenConflict(self, queen: tuple) -> int:
        """
        Get the number of conflicts for a queen.
        """
        (row, column) = queen
        # get row conflict
        numberOfAttacks = self.columnQueens.get(column) - 1
        # get right diagonal conflict
        numberOfAttacks += self.rightDiagonalQueens.get(column - row) - 1
        # get left diagonal conflict
        numberOfAttacks += self.leftDiagonalQueens.get(row + column) - 1

        return numberOfAttacks

    def solvedCheck(self) -> bool:
        """
        Check if the chessboard is solved.
        """
        if self.numberOfAttacks == 0:
            return True
        else:
            return False
