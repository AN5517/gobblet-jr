"""
Game class for Gobblet Jr.
"""

from .board import Board
from .player import Player

class Game:
    """Main game class for Gobblet Jr."""

    def __init__(self):
        """Initialize the game with board, players, and game state."""
        self.board = Board()
        self.players = [Player('red'), Player('yellow')]
        self.current_player_idx = 0
        self.moves_history = []
        self.game_over = False
        self.winner = None

    @property
    def current_player(self):
        """Get the current player."""
        return self.players[self.current_player_idx]

    def switch_player(self):
        """Switch to the next player."""
        self.current_player_idx = 1 - self.current_player_idx

    def make_move(self, piece_idx=None, from_pos=None, to_pos=None):
        """
        Make a move in the game.

        Args:
            piece_idx (int, optional): Index of piece to place from player's available pieces
            from_pos (tuple, optional): Position (row, col) to move piece from
            to_pos (tuple, optional): Position (row, col) to move/place piece to

        Returns:
            bool: True if the move was successful
        """
        if self.game_over:
            return False

        # Record state for history
        prev_state = self._get_state_snapshot()

        # Place new piece from player's supply
        if piece_idx is not None and from_pos is None:
            available_pieces = self.current_player.get_available_pieces()

            # Check if piece_idx is valid
            if piece_idx >= len(available_pieces):
                return False

            piece = available_pieces[piece_idx]
            to_row, to_col = to_pos

            # print(    # debug statement
            #     f"Attempting a move on {self.current_player.color} player's "
            #     f"available {['Small', 'Medium', 'Large'][piece.size]} piece, "
            #     f"from {from_pos} to {to_pos}."
            # )

            # Check if placement is valid
            current_piece = self.board.grid[to_row][to_col]
            if current_piece is None or piece.can_gobble(current_piece):
                piece = self.current_player.place_piece(piece_idx)
                self.board.place_piece(piece, to_row, to_col)
                self.moves_history.append(prev_state)
                self._check_game_end()
                self.switch_player()
                return True

        # Move piece already on the board
        elif from_pos is not None and to_pos is not None:
            from_row, from_col = from_pos
            to_row, to_col = to_pos

            # Verify the piece belongs to the current player
            if (self.board.grid[from_row][from_col] is not None and
                self.board.grid[from_row][from_col].color == self.current_player.color):

                if self.board.move_piece(from_row, from_col, to_row, to_col):
                    # Check if the move exposed a winning sequence for the opponent
                    winner = self.board.check_winner()
                    if winner and winner != self.current_player.color:
                        self.game_over = True
                        self.winner = winner
                    else:
                        # Proceed with normal game flow
                        self.moves_history.append(prev_state)
                        self._check_game_end()
                        self.switch_player()
                    return True

        return False

    def rewind(self):
        """
        Rewind the game by one move.

        Returns:
            bool: True if rewind was successful
        """
        if not self.moves_history:
            return False

        prev_state = self.moves_history.pop()
        self._restore_state(prev_state)
        return True

    def _get_state_snapshot(self):
        """
        Get a snapshot of the current game state.

        Returns:
            dict: Game state
        """
        # This is a simplified implementation - a real one would deep copy all game state
        # Right now, I kinda am deep copying all that's necessary for rewind
        return {
            'board': [row[:] for row in self.board.grid],
            'current_player_idx': self.current_player_idx,
            'game_over': self.game_over,
            'winner': self.winner,
            'available_pieces': {
                'red': self.players[0].get_available_pieces(),
                'yellow': self.players[1].get_available_pieces()
            }
        }

    def _restore_state(self, state):
        """
        Restore a previous game state.
        
        Args:
            state (dict): Game state to restore
        """
        # This is a simplified implementation - a real one would restore all game state
        self.board.grid = state['board']
        self.current_player_idx = state['current_player_idx']
        self.game_over = state['game_over']
        self.winner = state['winner']
        self.players[0].restore_available_pieces(state['available_pieces']['red'])
        self.players[1].restore_available_pieces(state['available_pieces']['yellow'])

    def _check_game_end(self):
        """Check if the game has ended."""
        winner = self.board.check_winner()
        if winner:
            self.game_over = True
            self.winner = winner
