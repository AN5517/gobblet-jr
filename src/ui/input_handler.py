import pygame
from .constants import BOARD_ORIGIN, CELL_SIZE, BOARD_ROWS, BOARD_COLS
from ..game.piece import Piece

class InputHandler:
    def __init__(self, game):
        self.game = game
        self.dragging = False
        self.dragged_piece = None
        self.drag_offset = (0, 0)
        self.mouse_pos = (0, 0)

    def handle_event(self, event):
        """
        Handle a pygame event (mouse down/up/motion).
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse down
                self._start_drag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse up
                self._stop_drag(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.mouse_pos = event.pos

    def get_dragging_info(self):
        """
        Returns (is_dragging, piece, position) for rendering a dragged piece.
        """
        return (self.dragging, self.dragged_piece, self.mouse_pos)

    def _start_drag(self, pos):
        """
        Begin dragging if user clicked on a piece (in board or player's area).
        """
        # Check if click is on the player's available pieces first
        for player_piece in self.game.current_player.get_available_pieces():
            # Rough bounding for each available piece in the area
            # We'll guess each piece is spaced 50 px in x-direction
            idx = self.game.current_player.get_available_pieces().index(player_piece)
            area_x = 20 + idx * 50
            area_y = 30
            # The player's area is offset from the constants (like (50, 400) or (450, 400))
            # We check both players if they are current, but typically only one matches
            # For simplicity, assume we only pick from the current player's location
            # Hard-coded offsets:
            base_x, base_y = (50, 400) if self.game.current_player.color == "red" else (450, 400)
            center_x = base_x + area_x
            center_y = base_y + area_y
            radius_map = {0: 20, 1: 30, 2: 40}
            radius = radius_map.get(player_piece.size, 20)
            dist = ((pos[0] - center_x)**2 + (pos[1] - center_y)**2) ** 0.5
            if dist <= radius:
                self.dragging = True
                self.dragged_piece = player_piece
                self.drag_offset = (0, 0)
                self.mouse_pos = pos
                return

        # Otherwise, check if click is on a piece on the board
        row = (pos[1] - BOARD_ORIGIN[1]) // CELL_SIZE
        col = (pos[0] - BOARD_ORIGIN[0]) // CELL_SIZE
        if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            piece = self.game.board.grid[row][col]
            if piece is not None and piece.color == self.game.current_player.color:
                self.dragging = True
                self.dragged_piece = piece
                # Offset from the top-left corner of that grid cell
                self.drag_offset = (pos[0] - (BOARD_ORIGIN[0] + col * CELL_SIZE),
                                    pos[1] - (BOARD_ORIGIN[1] + row * CELL_SIZE))
                self.mouse_pos = pos

    def _stop_drag(self, pos):
        """
        End dragging, attempt to make a move if dropped in a valid spot.
        """
        if self.dragging and self.dragged_piece:
            row = (pos[1] - BOARD_ORIGIN[1]) // CELL_SIZE
            col = (pos[0] - BOARD_ORIGIN[0]) // CELL_SIZE
            if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
                # If piece is still in player's leftover supply
                if self.dragged_piece in self.game.current_player.get_available_pieces():
                    piece_idx = self.game.current_player.get_available_pieces().index(self.dragged_piece)
                    self.game.make_move(piece_idx=piece_idx, to_pos=(row, col))
                else:
                    # Search the board for its current location
                    old_row, old_col = None, None
                    for r in range(BOARD_ROWS):
                        for c in range(BOARD_COLS):
                            if self.game.board.grid[r][c] == self.dragged_piece:
                                old_row, old_col = r, c
                                break
                        if old_row is not None:
                            break
                    if old_row is not None and old_col is not None:
                        self.game.make_move(from_pos=(old_row, old_col), to_pos=(row, col))
        self.dragging = False
        self.dragged_piece = None