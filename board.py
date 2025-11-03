import numpy as np


class Board:
    def __init__(self):
        # Initialize a 6x7 board (6 rows, 7 columns) filled with zeros
        self.board = np.zeros((6, 7), dtype="i")

    # Print the board to test
    def print_board(self):
        print(self.board[::-1])

    # Copy of the board to apply minimax algorithm
    def import_board(self, board):
        self.board = board

    # Check if a column has space for a new piece
    def valid_move(self, col):
        if self.board[5, col] != 0:
            return False
        return True

    # Drop a piece into the column
    def make_move(self, col, player):
        if self.valid_move(col):
            for i in range(6):
                if self.board[i, col] == 0:
                    self.board[i, col] = player
                    break

    # Return a list of all columns where a piece can be placed
    def available_locations(self):
        available_locations = []

        for i in range(7):
            if self.valid_move(i):
                available_locations.append(i)

        return available_locations

    # Check if the game has ended
    def is_terminal_board(self):
        return self.check_win() or len(self.available_locations()) == 0

    # Check all possible winning conditions
    def check_win(self):
        # Horizontal check
        for col in range(6):
            for row in range(4):
                if self.board[col, row] == self.board[col, row + 1] == self.board[col, row + 2] == self.board[col, row + 3] != 0:
                    return self.board[col, row]

        # Vertical check
        for col in range(3):
            for row in range(7):
                if self.board[col, row] == self.board[col + 1, row] == self.board[col + 2, row] == self.board[col + 3, row] != 0:
                    return self.board[col, row]

        # Positive diagonal check
        for col in range(3):
            for row in range(4):
                if self.board[col, row] == self.board[col + 1, row + 1] == self.board[col + 2, row + 2] == self.board[col + 3, row + 3] != 0:
                    return self.board[col, row]

        # Negative diagonal check
        for col in range(5, 2, -1):
            for row in range(4):
                if self.board[col, row] == self.board[col - 1, row + 1] == self.board[col - 2, row + 2] == self.board[col - 3, row + 3] != 0:
                    return self.board[col, row]

        return 0