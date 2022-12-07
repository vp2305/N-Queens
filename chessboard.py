import random
from copy import deepcopy
import numpy as np


# For loop - createChessboard - Good enough, getNumberOfAttacks, updateColumnDiagonalQueens, minConflict, conflicts, getConflictedQueen, printChessboard
class Chess:
    def __init__(self, height, width, maxSteps) -> None:
        self.height = height
        self.width = width
        self.maxSteps = maxSteps
        self.numberOfQueens = height
        self.grid = []
        self.queens = []
        self.rowQueens = {}
        self.rightDiagonalQueens = {}
        self.leftDiagonalQueens = {}
        self.numberOfAttacks = -1
        self.createChessboard()
        self.updateColumnDiagonalQueens()
        self.getNumberOfAttacks()

    def solvedCheck(self) -> bool:
        """
        Check if the chessboard is solved.
        """
        if self.numberOfAttacks == 0:
            return True
        else:
            return False

    def createChessboard(self) -> None:
        """
        Create the chessboard and place queens.
        """
        print("Creating chessboard...")

        random_indices = random.sample(range(self.height), k=self.width)
        self.grid = np.zeros((self.height, self.width), dtype=int)

        for idx in random_indices:
            self.grid[idx, random_indices[idx]] = 1
            self.queens.append((idx, random_indices[idx]))

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
            self.numberOfAttacks += self.rowQueens.get(row) - 1
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
            self.rowQueens[row] = self.rowQueens.get(row, 0) + 1
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
                print(
                    f"\nChessboard solved in {i} steps for {len(self.queens)} queens."
                )
                return True
            else:
                print(f"Step {i}:")
                conflictedQueen: tuple = self.getConflictedQueen()
                self.conflicts(conflictedQueen)
                print("Number of attacking queens: ", self.numberOfAttacks)
                # self.printChessboard()

        # If the chessboard is not solved after max steps, return false.
        print(f"\nChessboard not solved\nTry increasing max steps.")
        print(f"Number of queens: {len(self.queens)}")
        return False

    def conflicts(self, conflictedQueen: tuple):
        """
        Determine a move that will minimize the number of conflicts.
        """
        # We get the conflictedQueen
        (row, column) = conflictedQueen
        # Get the current conflict for the conflictQueen.
        minConflict = self.getQueenConflict(conflictedQueen)
        # minNumberOfAttacks = deepcopy(self.numberOfAttacks)
        # Store the coordinate of the queen with the least conflict.
        minConflictCoordinate = conflictedQueen

        # Go through all the columns and find the column with the least conflict.
        for i in range(self.height):
            if i != column:
                # Move the conflicted queen to the new destination within the column of the conflicted queen.
                self.moveQueen(conflictedQueen, (i, column))
                # Get the number of conflicts for the queen.
                currentConflict = self.getQueenConflict((i, column))
                # If the current conflict is less than the minimum conflict, update the minimum conflict.
                if currentConflict < minConflict:
                    minConflict = currentConflict
                    minConflictCoordinate = (i, column)
                    self.queens.remove(conflictedQueen)
                    self.queens.append(minConflictCoordinate)
                    return

                # If the current conflict is the same as the minimum conflict, choose a random column.
                elif currentConflict == minConflict:
                    if random.randint(0, 1):
                        minConflictCoordinate = (i, column)
                # Move the queen back to the original position.
                self.moveQueen((i, column), conflictedQueen)

        # If we don't find a column with less conflict, we move the queen to a random column.
        self.moveQueen(conflictedQueen, minConflictCoordinate)
        # Update the queen's position.
        self.queens.remove(conflictedQueen)
        self.queens.append(minConflictCoordinate)

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
            random.randint(0, len(mostConflictedQueenList) - 1)
        ]

        return conflictedQueen

    def moveQueen(self, queen: tuple, newPosition: tuple) -> None:
        """
        Move a queen to a new column.
        """
        (row, column) = queen
        (newRow, newColumn) = newPosition
        previousQueenConflict = self.getQueenConflict(queen)

        # Remove the queen from the column and diagonal queens.
        self.rowQueens[row] -= 1
        self.rightDiagonalQueens[column - row] -= 1
        self.leftDiagonalQueens[row + column] -= 1

        # Move the queen to the new column.
        self.grid[row][column] = 0
        self.grid[newRow][newColumn] = 1

        # Update the column and diagonal queens.
        self.rowQueens[newRow] = self.rowQueens.get(newRow, 0) + 1
        self.rightDiagonalQueens[newColumn - newRow] = (
            self.rightDiagonalQueens.get((newColumn - newRow), 0) + 1
        )
        self.leftDiagonalQueens[newRow + newColumn] = (
            self.leftDiagonalQueens.get((newRow + newColumn), 0) + 1
        )

        # Update the number of attacks.
        newQueenConflict = self.getQueenConflict(newPosition)
        self.numberOfAttacks += newQueenConflict - previousQueenConflict

    def getQueenConflict(self, queen: tuple) -> int:
        """
        Get the number of conflicts for a queen.
        """
        (row, column) = queen
        # get row conflict
        numberOfAttacks = self.rowQueens.get(row) - 1
        # get right diagonal conflict
        numberOfAttacks += self.rightDiagonalQueens.get(column - row) - 1
        # get left diagonal conflict
        numberOfAttacks += self.leftDiagonalQueens.get(row + column) - 1

        return numberOfAttacks
