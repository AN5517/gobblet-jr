import pygame
from .constants import *

class Renderer:
    """Handles rendering of game elements."""
    
    def __init__(self, screen):
        """
        Initialize the renderer.
        
        Args:
            screen (pygame.Surface): The pygame display surface
        """
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        
    def draw_board(self):
        """Draw the game board."""
        # Draw board background
        pygame.draw.rect(
            self.screen, 
            LIGHT_BROWN, 
            (BOARD_POSITION[0], BOARD_POSITION[1], BOARD_SIZE, BOARD_SIZE)
        )
        
        # Draw grid lines
        for i in range(1, 3):
            # Vertical lines
            pygame.draw.line(
                self.screen,
                DARK_BROWN,
                (BOARD_POSITION[0] + i * CELL_SIZE, BOARD_POSITION[1]),
                (BOARD_POSITION[0] + i * CELL_SIZE, BOARD_POSITION[1] + BOARD_SIZE),
                3
            )
            # Horizontal lines
            pygame.draw.line(
                self.screen,
                DARK_BROWN,
                (BOARD_POSITION[0], BOARD_POSITION[1] + i * CELL_SIZE),
                (BOARD_POSITION[0] + BOARD_SIZE, BOARD_POSITION[1] + i * CELL_SIZE),
                3
            )
    
    def draw_piece(self, piece, x, y, highlight=False):
        """
        Draw a game piece.
        
        Args:
            piece (Piece): The piece to draw
            x (int): X-coordinate center of the piece
            y (int): Y-coordinate center of the piece
            highlight (bool): Whether to highlight the piece
        """
        if piece is None:
            return
            
        color = RED if piece.color == 'red' else YELLOW
        radius = PIECE_SIZES[piece.size]
        
        # Draw piece shadow
        pygame.draw.circle(self.screen, GRAY, (x + 3, y + 3), radius)
        
        # Draw piece
        pygame.draw.circle(self.screen, color, (x, y), radius)
        
        # Draw highlight if needed
        if highlight:
            pygame.draw.circle(self.screen, WHITE, (x, y), radius, 2)
    
    def draw_board_pieces(self, board):
        """
        Draw all pieces on the board.
        
        Args:
            board (Board): The game board
        """
        for row in range(3):
            for col in range(3):
                piece = board.grid[row][col]
                if piece:
                    x = BOARD_POSITION[0] + col * CELL_SIZE + CELL_SIZE // 2
                    y = BOARD_POSITION[1] + row * CELL_SIZE + CELL_SIZE // 2
                    self.draw_piece(piece, x, y)
    
    def draw_player_area(self, player, position, current_player=False):
        """
        Draw player's area with available pieces.
        
        Args:
            player (Player): The player whose area to draw
            position (tuple): Top-left position of the player area
            current_player (bool): Whether this is the current player
        """
        x, y = position
        
        # Draw player area background
        pygame.draw.rect(
            self.screen,
            LIGHT_GRAY if current_player else WHITE,
            (x, y, PLAYER_AREA_WIDTH, PLAYER_AREA_HEIGHT)
        )
        
        # Draw player name
        text = self.font.render(f"{player.color.capitalize()}", True, BLACK)
        self.screen.blit(text, (x + 20, y + 20))
        
        # Draw available pieces
        pieces = player.get_available_pieces()
        for i, piece in enumerate(pieces):
            piece_x = x + PLAYER_AREA_WIDTH // 2
            piece_y = y + 80 + i * PIECE_SPACING
            self.draw_piece(piece, piece_x, piece_y)
    
    def draw_buttons(self):
        """Draw the control buttons."""
        # Draw rewind button
        pygame.draw.rect(
            self.screen,
            LIGHT_GRAY,
            (REWIND_BUTTON_POSITION[0], REWIND_BUTTON_POSITION[1], BUTTON_WIDTH, BUTTON_HEIGHT)
        )
        text = self.font.render("<", True, BLACK)
        self.screen.blit(text, (REWIND_BUTTON_POSITION[0] + 30, REWIND_BUTTON_POSITION[1] + 10))
        
        # Draw replay button
        pygame.draw.rect(
            self.screen,
            LIGHT_GRAY,
            (REPLAY_BUTTON_POSITION[0], REPLAY_BUTTON_POSITION[1], BUTTON_WIDTH, BUTTON_HEIGHT)
        )
        text = self.font.render(">", True, BLACK)
        self.screen.blit(text, (REPLAY_BUTTON_POSITION[0] + 30, REPLAY_BUTTON_POSITION[1] + 10))
    
    def draw_game_status(self, game):
        """
        Draw the game status.
        
        Args:
            game (Game): The current game
        """
        if game.game_over:
            message = f"{game.winner.capitalize()} wins!"
        else:
            message = f"{game.current_player.color.capitalize()}'s turn"
        
        text = self.font.render(message, True, BLACK)
        self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 50))
    
    def draw_dragging_piece(self, piece, pos):
        """
        Draw a piece being dragged.
        
        Args:
            piece (Piece): The piece being dragged
            pos (tuple): Current mouse position
        """
        self.draw_piece(piece, pos[0], pos[1], highlight=True)