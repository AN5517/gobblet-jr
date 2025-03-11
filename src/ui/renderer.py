import pygame
from .constants import (
    BLACK, GRAY, RED, YELLOW, BOARD_ORIGIN,
    CELL_SIZE, BOARD_ROWS, BOARD_COLS,
    BUTTON_WIDTH, BUTTON_HEIGHT
)

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20)
        
        # A single "Rewind" button at the top-left
        self.button_rewind_rect = pygame.Rect(10, 10, BUTTON_WIDTH, BUTTON_HEIGHT)

    def draw_board(self):
        """
        Draw the 3x3 board grid.
        """
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                rect_x = BOARD_ORIGIN[0] + col * CELL_SIZE
                rect_y = BOARD_ORIGIN[1] + row * CELL_SIZE
                cell_rect = pygame.Rect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GRAY, cell_rect, 2)

    def draw_board_pieces(self, board):
        """
        Draw pieces on the board.
        """
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                piece = board.grid[row][col]
                if piece is not None:
                    self._draw_piece(piece, row, col)

    def _draw_piece(self, piece, row, col):
        """
        Draw a single piece at its board position.
        Piece size: 0=small, 1=medium, 2=large.
        """
        color = RED if piece.color == "red" else YELLOW
        radius_map = {0: 20, 1: 30, 2: 40}
        radius = radius_map.get(piece.size, 20)

        center_x = BOARD_ORIGIN[0] + col * CELL_SIZE + CELL_SIZE // 2
        center_y = BOARD_ORIGIN[1] + row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(self.screen, color, (center_x, center_y), radius)

    def draw_player_area(self, player, position, current_player=False):
        """
        Draw the pieces area for a player.
        """
        label = f"Player {player.color.capitalize()}"
        if current_player:
            label += " (Your Turn)"
        text_surf = self.font.render(label, True, BLACK)
        self.screen.blit(text_surf, position)

        # Render each available piece in a row
        x_off = position[0]
        y_off = position[1] + 30
        for idx, piece in enumerate(player.get_available_pieces()):
            color = RED if piece.color == "red" else YELLOW
            radius_map = {0: 20, 1: 30, 2: 40}
            radius = radius_map.get(piece.size, 20)
            circ_x = x_off + 20 + idx * 50
            circ_y = y_off
            pygame.draw.circle(self.screen, color, (circ_x, circ_y), radius)

    def draw_buttons(self):
        """
        Draw only the rewind button.
        """
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
        Display game status (winner or current turn).
        """
        status_str = ""
        if game.game_over:
            if game.winner:
                status_str = f"Game Over! Winner: {game.winner}"
            else:
                status_str = "Game Over! No winner"
        else:
            status_str = f"Current Turn: {game.current_player.color}"

        text_surf = self.font.render(status_str, True, BLACK)
        self.screen.blit(text_surf, (250, 10))

    def draw_dragging_piece(self, piece, pos):
        """
        Draw a piece currently being dragged.
        """
        color = RED if piece.color == "red" else YELLOW
        radius_map = {0: 20, 1: 30, 2: 40}
        radius = radius_map.get(piece.size, 20)
        pygame.draw.circle(self.screen, color, pos, radius)