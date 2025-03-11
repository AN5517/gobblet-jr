import pygame
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game.game import Game
from src.ui.renderer import Renderer
from src.ui.input_handler import InputHandler
from src.ui.constants import *

def main():
    """Main function to run the Gobblet Jr. game."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    # Initialize game components
    game = Game()
    renderer = Renderer(screen)
    input_handler = InputHandler(game)
    
    running = True
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            input_handler.handle_event(event)
        
        # Clear the screen
        screen.fill(WHITE)
        
        # Draw game elements
        renderer.draw_board()
        renderer.draw_board_pieces(game.board)
        
        # Draw player areas
        renderer.draw_player_area(
            game.players[0], 
            PLAYER1_AREA_POSITION, 
            current_player=(game.current_player_idx == 0)
        )
        renderer.draw_player_area(
            game.players[1], 
            PLAYER2_AREA_POSITION, 
            current_player=(game.current_player_idx == 1)
        )
        
        # Draw buttons
        renderer.draw_buttons()
        
        # Draw game status
        renderer.draw_game_status(game)
        
        # Draw dragged piece if any
        is_dragging, piece, pos = input_handler.get_dragging_info()
        if is_dragging and piece:
            renderer.draw_dragging_piece(piece, pos)
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()