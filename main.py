from chessboard import Chess


def main():
    """
    Main function.
    """
    # n = int(input("Enter the number of queens: "))
    n = 10000
    # Create a new instance of the class
    chessboard = Chess(height=n, width=n, maxSteps=10000)
    # Print the chessboard
    # chessboard.printChessboard()
    chessboard.minConflict()


main()
print()
