"""
This module handles mouse input events for the game.
"""

import pygame
from .constants import BOARD_ORIGIN, CELL_SIZE, BOARD_ROWS, BOARD_COLS

class InputHandler:
    """Handles mouse input events for the game."""
    
    def __init__(self, game):
        self.game = game
        self.dragging = False
        self.dragged_piece = None
        self.mouse_pos = (0, 0)

    def handle_event(self, event):
        """Handle mouse events for picking up and dropping pieces."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._start_drag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._stop_drag(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.mouse_pos = event.pos

    def get_dragging_info(self):
        """Return (is_dragging, piece, position) for rendering a dragged piece."""
        return (self.dragging, self.dragged_piece, self.mouse_pos)

    def cancel_drag(self):
        """Cancel any ongoing drag operation."""
        self.dragging = False
        self.dragged_piece = None

    def _start_drag(self, pos):
        """Check if the current player clicked on a piece (board or supply) to drag."""
        if self.game.game_over:
            return

        current_player = self.game.current_player
        # Check if click is on player's available pieces
        for (idx, piece) in enumerate(current_player.get_available_pieces()):
            # Estimate rough bounding circle for each piece
            # Player area positions come from the renderer's known layout
            if current_player.color == 'red':
                base_x, base_y = (50, 440)
            else:
                base_x, base_y = (450, 440)

            piece_x = base_x + 20 + idx * 50
            piece_y = base_y
            radius_map = {0: 20, 1: 30, 2: 40}
            radius = radius_map.get(piece.size, 20)
            dist = ((pos[0] - piece_x)**2 + (pos[1] - piece_y)**2)**0.5
            if dist <= radius:
                self.dragging = True
                self.dragged_piece = piece
                self.mouse_pos = pos
                return

        # Check board pieces
        row = (pos[1] - BOARD_ORIGIN[1]) // CELL_SIZE
        col = (pos[0] - BOARD_ORIGIN[0]) // CELL_SIZE
        if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            piece = self.game.board.grid[row][col]
            if piece and piece.color == current_player.color:
                self.dragging = True
                self.dragged_piece = piece
                self.mouse_pos = pos

    def _stop_drag(self, pos):
        """Drop the piece, if valid, and let the game handle the move."""
        if not self.dragging or not self.dragged_piece or self.game.game_over:
            self.cancel_drag()
            return

        row = (pos[1] - BOARD_ORIGIN[1]) // CELL_SIZE
        col = (pos[0] - BOARD_ORIGIN[0]) // CELL_SIZE

        # Attempt placing from supply
        if self.dragged_piece in self.game.current_player.get_available_pieces():
            if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
                current_player = self.game.current_player
                piece_idx = current_player.get_available_pieces().index(self.dragged_piece)
                self.game.make_move(piece_idx=piece_idx, to_pos=(row, col))
        else:
            # Attempt moving on the board
            # Find old pos
            old_row, old_col = None, None
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    if self.game.board.grid[r][c] == self.dragged_piece:
                        old_row, old_col = r, c
                        break
                if old_row is not None:
                    break

            if (
                old_row is not None
                and old_col is not None
                and 0 <= row < BOARD_ROWS
                and 0 <= col < BOARD_COLS
            ):
                self.game.make_move(from_pos=(old_row, old_col), to_pos=(row, col))

        self.cancel_drag()
