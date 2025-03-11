"""
This module contains the Board class, which represents the 3x3 game board for Gobblet Jr.
"""

class Board:
    """Represents the 3x3 game board for Gobblet Jr."""

    def __init__(self):
        """Initialize an empty 3x3 board."""
        self.grid = [[None for _ in range(3)] for _ in range(3)]

    def place_piece(self, piece, row, col):
        """
        Place a piece on the board at the given position.

        Args:
            piece (Piece): The piece to place
            row (int): Row index (0-2)
            col (int): Column index (0-2)

        Returns:
            bool: True if placement was successful
        """
        current_piece = self.grid[row][col]

        if current_piece is None or piece.can_gobble(current_piece):
            if current_piece is not None:
                piece.gobble(current_piece)
            self.grid[row][col] = piece
            return True
        return False

    def move_piece(self, from_row, from_col, to_row, to_col):
        """
        Move a piece from one position to another.

        Args:
            from_row (int): Source row index
            from_col (int): Source column index
            to_row (int): Destination row index
            to_col (int): Destination column index

        Returns:
            bool: True if move was successful
        """
        if from_row == to_row and from_col == to_col:
            return False

        piece = self.grid[from_row][from_col]
        if piece is None:
            return False

        # Try to place the piece at the destination
        to_piece = self.grid[to_row][to_col]
        if to_piece is None or piece.can_gobble(to_piece):
            # Temporarily store what's under the piece we're moving
            revealed_piece = piece.reveal()

            # If destination has a piece, gobble it
            if to_piece is not None:
                piece.gobble(to_piece)

            # Update the grid
            self.grid[to_row][to_col] = piece
            self.grid[from_row][from_col] = revealed_piece

            return True

        return False

    def check_winner(self):
        """
        Check if there's a winner.

        Returns:
            str or None: Color of winner ('red', 'yellow') or None if no winner
        """
        # Check rows
        for row in range(3):
            if (self.grid[row][0] is not None and
                self.grid[row][1] is not None and
                self.grid[row][2] is not None and
                self.grid[row][0].color == self.grid[row][1].color == self.grid[row][2].color):
                return self.grid[row][0].color

        # Check columns
        for col in range(3):
            if (self.grid[0][col] is not None and
                self.grid[1][col] is not None and
                self.grid[2][col] is not None and
                self.grid[0][col].color == self.grid[1][col].color == self.grid[2][col].color):
                return self.grid[0][col].color

        # Check diagonals
        if (self.grid[0][0] is not None and
            self.grid[1][1] is not None and
            self.grid[2][2] is not None and
            self.grid[0][0].color == self.grid[1][1].color == self.grid[2][2].color):
            return self.grid[0][0].color

        if (self.grid[0][2] is not None and
            self.grid[1][1] is not None and
            self.grid[2][0] is not None and
            self.grid[0][2].color == self.grid[1][1].color == self.grid[2][0].color):
            return self.grid[0][2].color

        return None
