"""
Renderer class to handle rendering of the game board,
pieces, player areas, buttons, and game status.
"""

import pygame
from .constants import (
    BLACK, GRAY, RED, YELLOW, GREEN,
    BOARD_ORIGIN, CELL_SIZE, BOARD_ROWS, BOARD_COLS,
    BUTTON_WIDTH, BUTTON_HEIGHT,
    PLAYER1_LABEL_POSITION, PLAYER2_LABEL_POSITION,
    PLAYER1_PIECES_POSITION, PLAYER2_PIECES_POSITION
)

class Renderer:
    """Handles rendering of the game board, pieces, and UI elements."""
    
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20)
        self.font_big = pygame.font.SysFont("Arial", 26)

        # Buttons
        self.button_rewind_rect = pygame.Rect(10, 10, BUTTON_WIDTH, BUTTON_HEIGHT)

    def draw_board(self):
        """Draw the 3x3 board grid."""
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                rect_x = BOARD_ORIGIN[0] + col * CELL_SIZE
                rect_y = BOARD_ORIGIN[1] + row * CELL_SIZE
                cell_rect = pygame.Rect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GRAY, cell_rect, 2)

    def draw_board_pieces(self, board):
        """Draw all pieces on the board."""
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                piece = board.grid[row][col]
                if piece is not None:
                    self._draw_piece(piece, row, col)

    def _draw_piece(self, piece, row, col):
        """Draw a single piece at its board position with an outline."""
        color = RED if piece.color == "red" else YELLOW
        radius_map = {0: 20, 1: 30, 2: 40}
        radius = radius_map.get(piece.size, 20)

        center_x = BOARD_ORIGIN[0] + col * CELL_SIZE + CELL_SIZE // 2
        center_y = BOARD_ORIGIN[1] + row * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.circle(self.screen, color, (center_x, center_y), radius)
        pygame.draw.circle(self.screen, BLACK, (center_x, center_y), radius, 2)  # Outline

    def draw_player_area(self, player, label_position, pieces_position, current_player=False):
        """
        Draw the pieces area for a player, adjusting text and outline if current player's turn.
        """
        label = f"Player {player.color.capitalize()}"
        # font_to_use = self.font
        # label_offset = 0

        if current_player:
            label += " (Your Turn)"
            # label_offset = 4  # Extra space if big font

            # Draw a rectangle around the player's area
            highlight_rect = pygame.Rect(pieces_position[0] - 10, pieces_position[1] - 10, 320, 60)
            pygame.draw.rect(self.screen, BLACK, highlight_rect, 2)

        text_surface = self.font.render(label, True, BLACK)
        self.screen.blit(text_surface, label_position)

        # Render each available piece in a row below the label
        x_off = pieces_position[0]
        # y_off = pieces_position[1] + label_offset
        y_off = pieces_position[1]
        for idx, piece in enumerate(player.get_available_pieces()):
            color = RED if piece.color == "red" else YELLOW
            radius_map = {0: 20, 1: 30, 2: 40}
            radius = radius_map.get(piece.size, 20)

            circ_centre = (x_off + 20 + idx * 50, y_off)
            pygame.draw.circle(
                self.screen,
                RED if piece.color == "red" else YELLOW,
                circ_centre,
                radius
            )
            pygame.draw.circle(self.screen, BLACK, circ_centre, radius, 2)  # Outline

    def draw_buttons(self):
        """Draw the rewind button."""
        pygame.draw.rect(self.screen, GRAY, self.button_rewind_rect)
        rewind_text = self.font.render("Rewind", True, BLACK)
        self.screen.blit(
            rewind_text,
            (
                self.button_rewind_rect.centerx - rewind_text.get_width() // 2,
                self.button_rewind_rect.centery - rewind_text.get_height() // 2
            )
        )

    def draw_game_status(self, game):
        """
        Display game status.
        - If game over, text is green and shows winner.
        - Otherwise, show current player's color.
        """
        if game.game_over:
            if game.winner:
                status_str = f"Game Over! Winner: {game.winner}"
            else:
                status_str = "Game Over! No winner"
            text_color = GREEN
        else:
            status_str = f"Current Turn: {game.current_player.color}"
            text_color = BLACK

        text_surf = self.font.render(status_str, True, text_color)
        self.screen.blit(text_surf, (250, 10))

    def draw_dragging_piece(self, piece, pos):
        """Draw a piece currently being dragged, with dark outline."""
        color = RED if piece.color == "red" else YELLOW
        radius_map = {0: 20, 1: 30, 2: 40}
        radius = radius_map.get(piece.size, 20)

        pygame.draw.circle(self.screen, color, pos, radius)
        pygame.draw.circle(self.screen, BLACK, pos, radius, 2)  # Outline
