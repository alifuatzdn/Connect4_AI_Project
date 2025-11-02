=== Connect 4 AI Project ===

OVERVIEW
--------
This is a Connect 4 game implementation with an AI opponent using the Minimax algorithm with Alpha-Beta pruning.
The game features a graphical interface built with Pygame where a human player competes against an AI.

FEATURES
--------
- Interactive GUI using Pygame
- AI opponent using Minimax with Alpha-Beta pruning
- Configurable difficulty (search depth)
- Visual feedback and animations
- End-game screen with replay option

REQUIREMENTS
------------
- Python 3.7 or higher
- pygame
- numpy

INSTALLATION
------------
1. Clone or download this repository to your local machine

2. Install the required dependencies:
   pip install pygame numpy

RUNNING THE GAME
----------------
1. Navigate to the project directory:
   cd Connect4_AI_Project

2. Run the game:
   python game.py

   Note: The default difficulty is set to depth=2. You can modify the difficulty
   by changing the parameter in the last line of game.py:

HOW TO PLAY
-----------
- The player (RED) always goes first
- Move your mouse over the columns to preview your move
- Click on a column to drop your piece
- The AI (YELLOW) will automatically make its move
- Connect 4 pieces horizontally, vertically, or diagonally to win
- After the game ends, you can choose to play again or quit

PROJECT STRUCTURE
-----------------
game.py     - Main game loop and Pygame GUI implementation
board.py    - Board class with game logic and win detection
ai.py       - AI implementation with Minimax and scoring functions

GAME RULES
----------
- The game is played on a 6x7 grid
- Players alternate turns dropping colored pieces into columns
- Pieces fall to the lowest available position in the selected column
- The first player to get 4 pieces in a row (horizontal, vertical, or diagonal) wins
- If the board fills up with no winner, the game is a draw

AI IMPLEMENTATION
-----------------
The AI uses:
- Minimax algorithm with Alpha-Beta pruning for efficient search
- Heuristic evaluation function that considers:
  * Center column control
  * Potential winning patterns
  * Blocking opponent threats
  * Position scoring for strategic play