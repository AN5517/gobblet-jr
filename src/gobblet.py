"""
Main entry point for the Gobblet Jr. game.
To run the game, navigate to the `src` directory and run `python gobblet.py`.
"""

import sys
import os
import pygame

from game.game import Game
from ui.renderer import Renderer
from ui.input_handler import InputHandler
from ui.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TITLE, WHITE,
    PLAYER1_LABEL_POSITION, PLAYER2_LABEL_POSITION,
    PLAYER1_PIECES_POSITION, PLAYER2_PIECES_POSITION
)

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Main function to run the Gobblet Jr. game."""
    pygame.init()   # pylint: disable=no-member
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Initialize game components
    game = Game()
    renderer = Renderer(screen)
    input_handler = InputHandler(game)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # pylint: disable=no-member
                running = False

            # Check for clicks on the rewind button
            if (
                event.type == pygame.MOUSEBUTTONDOWN    # pylint: disable=no-member
                and event.button == 1
            ):
                if renderer.button_rewind_rect.collidepoint(event.pos):
                    # Attempt a rewind and cancel any dragging
                    if game.rewind():
                        input_handler.cancel_drag()

            # Pass event to input handler for dragging, etc.
            input_handler.handle_event(event)

        # Clear the screen
        screen.fill(WHITE)

        # Draw the board and pieces
        renderer.draw_board()
        renderer.draw_board_pieces(game.board)

        # Draw player areas
        renderer.draw_player_area(
            game.players[0],
            PLAYER1_LABEL_POSITION,
            PLAYER1_PIECES_POSITION,
            current_player=(game.current_player_idx == 0)
        )
        renderer.draw_player_area(
            game.players[1],
            PLAYER2_LABEL_POSITION,
            PLAYER2_PIECES_POSITION,
            current_player=(game.current_player_idx == 1)
        )

        # Draw the Rewind button
        renderer.draw_buttons()

        # Draw game status
        renderer.draw_game_status(game)

        # Draw any dragged piece
        is_dragging, piece, pos = input_handler.get_dragging_info()
        if is_dragging and piece:
            renderer.draw_dragging_piece(piece, pos)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()   # pylint: disable=no-member
    sys.exit()

if __name__ == "__main__":
    main()
