from chessboard import Chess

# Q. What is the time complexity of the minConflict function?
# A. O(n^2)


def main():
    """
    Main function.
    """
    # Create a new instance of the class
    chessboard = Chess(height=100000, width=100000, maxSteps=1000000)
    # Print the chessboard
    # chessboard.printChessboard()
    chessboard.minConflict()


main()
print()
