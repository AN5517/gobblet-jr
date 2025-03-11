# Gobblet Jr. Game

Gobblet Jr. is a strategic board game inspired by the classic game of tic-tac-toe, designed for two players. The objective is to align three pieces of your color in a row, either vertically, horizontally, or diagonally. The game features unique mechanics where players can stack pieces of different sizes, adding depth to the strategy.

## Project Structure

The project is (mainly) organized as follows:

```
gobblet-jr
├── src
│   ├── main.py
│   ├── game
│   │   ├── __init__.py
│   │   ├── board.py            # Board representation and logic
│   │   ├── piece.py            # Piece class with size and color properties
│   │   ├── player.py           # Player class to manage player pieces
│   │   └── game.py             # Main game logic and state management
│   └── ui
│       ├── __init__.py
│       ├── renderer.py         # Handles drawing game elements
│       ├── constants.py        # Color constants and UI configurations
│       └── input_handler.py    # Processes mouse and keyboard events
├── assets
│   └── fonts                   # Fonts for UI elements
│       └── ...
├── tests
│   ├── __init__.py
│   ├── test_board.py
│   ├── test_game.py
│   ├── test_piece.py
│   └── test_player.py
├── requirements.txt
└── README.md
```

## Game Rules

- Each player (red or yellow) starts with 6 pieces: two large, two medium, and two small.
- Players take turns placing or moving pieces on a 3x3 board.
- A piece can be placed on an empty space or on top of a smaller piece, "gobbling" it.
- Only visible pieces count towards winning.
- If a move exposes a winning sequence for the opponent, they win immediately.
- Players must move a piece if they touch it.

## Controls

- Click and drag pieces to take a turn.
- Use arrow keys to rotate the board.
- Use `-` and `=` to zoom in and out.
- Use `_` and `+` to adjust the game size.
- The `<` button rewinds the game by one turn, while the `>` button replays a turn.

## Assumptions

- The rewind feature is implemented, allowing players to undo moves.
- The game does not enforce the rule of mandatory movement upon touching a piece.

## Setup Instructions

1. Clone the repository.
2. Install the required dependencies listed in `requirements.txt`.
3. Run the game using `python src/main.py`.

Enjoy playing Gobblet Jr.!