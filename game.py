import pygame
from board import Board
import math
from ai import alpha_beta_minmax

# Constants for the game
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 3)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Screen options of the game
screen = pygame.display.set_mode((SQUARE_SIZE * 7, SQUARE_SIZE * 7))
pygame.display.set_caption("Connect Four")


def draw_table(board):
    for r in range(6):
        for c in range(7):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[5 - r, c]

            # Calculate x and y coordinates of the circle
            x = int(c * SQUARE_SIZE + SQUARE_SIZE / 2)
            y = int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)

            # Indicate the piece type
            if piece == 0:
                color = BLACK
            elif piece == 1:
                color = RED
            else:
                color = YELLOW

            pygame.draw.circle(screen, color, (x, y), RADIUS)

    pygame.display.update()


def draw_try_again_screen(winner):
    # Draw semi-transparent overlay to see the last state of the game
    overlay = pygame.Surface((SQUARE_SIZE * 7, SQUARE_SIZE * 7))
    overlay.set_alpha(220)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    # Indicate winner message
    if winner == 0:
        msg = "Draw!"
        color = (200, 200, 200)
    elif winner == 1:
        msg = "You Win!"
        color = RED
    else:
        msg = "AI Wins!"
        color = YELLOW

    # Display winner message
    font_title = pygame.font.SysFont("Arial", 60, bold=True)
    title_text = font_title.render(msg, True, color)
    title_rect = title_text.get_rect(center=(SQUARE_SIZE * 3.5, SQUARE_SIZE * 2))
    screen.blit(title_text, title_rect)

    # Button settings
    button_width = 200
    button_height = 70
    button_font = pygame.font.SysFont("Arial", 36)

    # Try again button
    try_again_rect = pygame.Rect(SQUARE_SIZE, SQUARE_SIZE * 3.5, button_width, button_height)
    pygame.draw.rect(screen, GREEN, try_again_rect)
    try_text = button_font.render("Try Again", True, BLACK)
    screen.blit(try_text, try_text.get_rect(center=try_again_rect.center))

    # Quit button
    quit_rect = pygame.Rect(SQUARE_SIZE * 4, SQUARE_SIZE * 3.5, button_width, button_height)
    pygame.draw.rect(screen, RED, quit_rect)
    quit_text = button_font.render("Quit", True, BLACK)
    screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

    pygame.display.update()
    return try_again_rect, quit_rect


def play_game(depth):
    # Initial conditions of the game
    game_board = Board()
    draw_table(game_board.board)
    run_game = True

    # We always start first to take advantage
    player = 1

    while run_game:
        # Take user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Display the piece dynamically
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, 700, SQUARE_SIZE))
                posx = event.pos[0]
                if player == 1:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
                pygame.display.update()

            # Check if the user clicked above any column
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, 700, SQUARE_SIZE))

                if player == 1:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARE_SIZE))

                    # Check the validity of move and update game control
                    if game_board.valid_move(col):
                        game_board.make_move(col, player)
                        draw_table(game_board.board)
                        player += 1
                        break

        if player == 2:
            # Select the optimal move for the opponent (AI)
            col, minimax_score = alpha_beta_minmax(game_board, depth, -math.inf, math.inf, True)

            if not game_board.is_terminal_board() and game_board.valid_move(col):
                pygame.time.wait(1000)
                game_board.make_move(col, player)
                draw_table(game_board.board)
                player -= 1

        if game_board.is_terminal_board():
            winner = game_board.check_win()
            try_again_rect, quit_rect = draw_try_again_screen(winner)

            # Check if the player wants to play again
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos

                        if try_again_rect.collidepoint(mouse_pos):
                            return True
                        elif quit_rect.collidepoint(mouse_pos):
                            return False

    return False


def game(difficulty):
    pygame.init()

    while True:
        play_again = play_game(difficulty)

        if not play_again:
            break

    pygame.quit()


game(2)
