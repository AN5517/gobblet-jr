import pygame
from .constants import *

class InputHandler:
    """Handles user input for the game."""
    
    def __init__(self, game):
        """
        Initialize the input handler.
        
        Args:
            game (Game): The game instance to handle input for
        """
        self.game = game
        self.dragging = False
        self.dragged_piece = None
        self.dragged_from = None
        self.dragged_from_board = False
        self.dragged_player_piece_idx = None
    
    def handle_event(self, event):
        """
        Handle a pygame event.
        
        Args:
            event (pygame.event.Event): The event to handle
            
        Returns:
            bool: True if the event was handled
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_down(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            return self._handle_mouse_up(event.pos)
        elif event.type == pygame.KEYDOWN:
            return self._handle_key_down(event.key)
        return False
    
    def _handle_mouse_down(self, pos):
        """
        Handle mouse button down event.
        
        Args:
            pos (tuple): Mouse position (x, y)
            
        Returns:
            bool: True if the event was handled
        """
        x, y = pos
        
        # Check if clicked on the board
        if (BOARD_POSITION[0] <= x <= BOARD_POSITION[0] + BOARD_SIZE and
            BOARD_POSITION[1] <= y <= BOARD_POSITION[1] + BOARD_SIZE):
            
            # Convert to board coordinates
            col = (x - BOARD_POSITION[0]) // CELL_SIZE
            row = (y - BOARD_POSITION[1]) // CELL_SIZE
            
            piece = self.game.board.grid[row][col]
            if piece and piece.color == self.game.current_player.color:
                self.dragging = True
                self.dragged_piece = piece
                self.dragged_from = (row, col)
                self.dragged_from_board = True
                return True
        
        # Check if clicked on player's pieces
        player = self.game.current_player
        player_pos = PLAYER1_AREA_POSITION if player.color == 'red' else PLAYER2_AREA_POSITION
        
        if (player_pos[0] <= x <= player_pos[0] + PLAYER_AREA_WIDTH and
            player_pos[1] <= y <= player_pos[1] + PLAYER_AREA_HEIGHT):
            
            pieces = player.get_available_pieces()
            for i, piece in enumerate(pieces):
                piece_x = player_pos[0] + PLAYER_AREA_WIDTH // 2
                piece_y = player_pos[1] + 80 + i * PIECE_SPACING
                
                # Check if clicked on this piece
                radius = PIECE_SIZES[piece.size]
                if ((x - piece_x) ** 2 + (y - piece_y) ** 2) <= radius ** 2:
                    self.dragging = True
                    self.dragged_piece = piece
                    self.dragged_player_piece_idx = i
                    self.dragged_from_board = False
                    return True
        
        # Check if clicked on buttons
        if (REWIND_BUTTON_POSITION[0] <= x <= REWIND_BUTTON_POSITION[0] + BUTTON_WIDTH and
            REWIND_BUTTON_POSITION[1] <= y <= REWIND_BUTTON_POSITION[1] + BUTTON_HEIGHT):
            self.game.rewind()
            return True
            
        if (REPLAY_BUTTON_POSITION[0] <= x <= REPLAY_BUTTON_POSITION[0] + BUTTON_WIDTH and
            REPLAY_BUTTON_POSITION[1] <= y <= REPLAY_BUTTON_POSITION[1] + BUTTON_HEIGHT):
            # Replay functionality would be implemented here
            return True
            
        return False
    
    def _handle_mouse_up(self, pos):
        """
        Handle mouse button up event.
        
        Args:
            pos (tuple): Mouse position (x, y)
            
        Returns:
            bool: True if the event was handled
        """
        if not self.dragging:
            return False
            
        x, y = pos
        self.dragging = False
        
        # Check if released on the board
        if (BOARD_POSITION[0] <= x <= BOARD_POSITION[0] + BOARD_SIZE and
            BOARD_POSITION[1] <= y <= BOARD_POSITION[1] + BOARD_SIZE):
            
            # Convert to board coordinates
            col = (x - BOARD_POSITION[0]) // CELL_SIZE
            row = (y - BOARD_POSITION[1]) // CELL_SIZE
            
            if self.dragged_from_board:
                # Moving piece on the board
                self.game.make_move(from_pos=self.dragged_from, to_pos=(row, col))
            else:
                # Placing new piece from player's supply
                self.game.make_move(piece_idx=self.dragged_player_piece_idx, to_pos=(row, col))
                
        # Reset dragging state
        self.dragged_piece = None
        self.dragged_from = None
        self.dragged_player_piece_idx = None
        
        return True
    
    def _handle_key_down(self, key):
        """
        Handle key down event.
        
        Args:
            key (int): Key code
            
        Returns:
            bool: True if the event was handled
        """
        # Handle arrow keys for board rotation (simplified version)
        if key == pygame.K_LEFT or key == pygame.K_RIGHT or key == pygame.K_UP or key == pygame.K_DOWN:
            # Board rotation would be implemented here
            return True
            
        # Handle zoom keys
        if key == pygame.K_MINUS or key == pygame.K_EQUALS:
            # Zoom would be implemented here
            return True
            
        return False
    
    def get_dragging_info(self):
        """
        Get information about the currently dragged piece.
        
        Returns:
            tuple: (is_dragging, piece, mouse_pos)
        """
        return self.dragging, self.dragged_piece, pygame.mouse.get_pos()