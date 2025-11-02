import math
import random
from board import Board
import numpy as np


def evaluate_score(board, player):
    score = 0

    # Center columns provide more advantage
    center_count = np.count_nonzero(board[:, 3] == player)
    score += center_count * 25

    # Horizontal check
    for col in range(4):
        for row in range(6):
            adjacent_places = [board[row, col], board[row, col + 1], board[row, col + 2], board[row, col + 3]]
            score += evaluate_adjacents(adjacent_places, player)

    # Vertical check
    for col in range(7):
        for row in range(3):
            adjacent_places = [board[row, col], board[row + 1, col], board[row + 2, col], board[row + 3, col]]
            score += evaluate_adjacents(adjacent_places, player)

    # Positive diagonal check
    for col in range(4):
        for row in range(3):
            adjacent_places = [board[row, col], board[row + 1, col + 1], board[row + 2, col + 2], board[row + 3, col + 3]]
            score += evaluate_adjacents(adjacent_places, player)

    # Negative diagonal check
    for col in range(4):
        for row in range(5, 2, -1):
            adjacent_places = [board[row, col], board[row - 1, col + 1], board[row - 2, col + 2], board[row - 3, col + 3]]
            score += evaluate_adjacents(adjacent_places, player)

    return score


def evaluate_adjacents(adjacent_places, player):
    opponent = 1 if player == 2 else 2
    score = 0

    # Count pieces for each player and empty spaces
    player_pieces = adjacent_places.count(player)
    opponent_pieces = adjacent_places.count(opponent)
    empty_pieces = adjacent_places.count(0)

    # Reward player's potential winning positions
    if player_pieces == 4:
        score += 1000
    elif player_pieces == 3 and empty_pieces == 1:
        score += 100
    elif player_pieces == 2 and empty_pieces == 2:
        score += 10

    # Penalize opponent's threatening positions
    if opponent_pieces == 3 and empty_pieces == 1:
        score -= 200
    elif opponent_pieces == 2 and empty_pieces == 2:
        score -= 15

    return score


def copy_board(board_obj, col, player):
    new_board = Board()
    # Copy the numpy array to avoid mutating the original
    new_board.import_board(board_obj.board.copy())
    new_board.make_movement(col, player)
    return new_board


def alpha_beta_minmax(board, depth, alpha, beta, maxim):
    available_locations = board.available_locations()
    is_terminal = board.is_terminal_board()

    # Base case: reached maximum depth or game ended
    if depth == 0 or is_terminal:
        if is_terminal:
            winner = board.check_win()
            if winner == 1:
                return None, -1000000000
            elif winner == 2:
                return None, 1000000000
            else:
                return None, 0
        else:
            # Evaluate board position using heuristic function
            return None, evaluate_score(board.board, 2)

    # Maximizing player (AI - player 2)
    if maxim:
        value = -math.inf
        # In case every column has the same score, choose randomly
        column = random.choice(available_locations)

        for col in available_locations:
            # Simulate opponent's move
            next_board = copy_board(board, col, 2)
            new_score = alpha_beta_minmax(next_board, depth - 1, alpha, beta, False)[1]

            # Update best move if better score found
            if new_score > value:
                value = new_score
                column = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return column, value

    # Minimizing player (opponent - player 1)
    else:
        value = math.inf
        column = random.choice(available_locations)

        for col in available_locations:
            # Simulate opponent's move
            next_board = copy_board(board, col, 1)
            new_score = alpha_beta_minmax(next_board, depth - 1, alpha, beta, True)[1]

            # Update worst move for AI (best for opponent)
            if new_score < value:
                value = new_score
                column = col

            # Alpha-beta pruning
            beta = min(beta, value)
            if alpha >= beta:
                break

        return column, value
