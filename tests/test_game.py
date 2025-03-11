import unittest
from src.game.game import Game
from src.game.piece import Piece, Size

class TestGame(unittest.TestCase):
    """Test cases for the Game class."""

    def setUp(self):
        """Set up a new game before each test."""
        self.game = Game()
    
    def test_init(self):
        """Test game initialization."""
        self.assertEqual(len(self.game.players), 2)
        self.assertEqual(self.game.players[0].color, "red")
        self.assertEqual(self.game.players[1].color, "yellow")
        self.assertEqual(self.game.current_player_idx, 0)
        self.assertIsNotNone(self.game.board)
        self.assertEqual(len(self.game.moves_history), 0)
    
    def test_switch_player(self):
        """Test switching players."""
        initial_player = self.game.current_player
        self.game.switch_player()
        self.assertNotEqual(self.game.current_player, initial_player)
        self.game.switch_player()
        self.assertEqual(self.game.current_player, initial_player)
    
    def test_make_move_new_piece(self):
        """Test placing a new piece from player's supply."""
        player = self.game.current_player
        initial_pieces_count = len(player.pieces)
        
        # Place a new piece
        result = self.game.make_move(piece_idx=0, to_pos=(0, 0))
        self.assertTrue(result)
        
        # Check piece was placed and player switched
        self.assertEqual(len(player.pieces), initial_pieces_count - 1)
        self.assertIsNotNone(self.game.board.grid[0][0])
        self.assertEqual(self.game.board.grid[0][0].color, player.color)
        self.assertNotEqual(self.game.current_player, player)  # Player should have switched
    
    def test_make_move_board_piece(self):
        """Test moving a piece already on the board."""
        # First place a piece
        self.game.make_move(piece_idx=0, to_pos=(1, 1))
        
        # Switch back to the first player
        self.game.switch_player()
        player = self.game.current_player
        
        # Now move that piece
        result = self.game.make_move(from_pos=(1, 1), to_pos=(2, 2))
        self.assertTrue(result)
        
        # Check the piece was moved
        self.assertIsNone(self.game.board.grid[1][1])
        self.assertIsNotNone(self.game.board.grid[2][2])
        self.assertEqual(self.game.board.grid[2][2].color, player.color)
    
    def test_invalid_moves(self):
        """Test invalid moves are rejected."""
        # Try moving from an empty position
        result = self.game.make_move(from_pos=(0, 0), to_pos=(1, 1))
        self.assertFalse(result)
        
        # Try placing a piece on a non-empty position that can't be gobbled
        self.game.make_move(piece_idx=0, to_pos=(0, 0))  # Place large piece
        self.game.switch_player()
        
        # The small piece is likely at index 4 or 5, not beyond the range
        # Make sure we're using a valid piece index
        small_piece_idx = len(self.game.current_player.pieces) - 1
        result = self.game.make_move(piece_idx=small_piece_idx, to_pos=(0, 0))  # Try to place small piece on top
        self.assertFalse(result)
    
    def test_winning_condition(self):
        """Test winning scenario."""

        # print(f"{self.game.players[0].color} pieces: ", *[x.size for x in self.game.players[0].pieces], sep=" ")
        # print(f"{self.game.players[1].color} pieces: ", *[x.size for x in self.game.players[1].pieces], sep=" ")
        
        # First move by Red
        self.game.make_move(piece_idx=0, to_pos=(0, 0))  # Red piece (large)
        self.game.make_move(piece_idx=0, to_pos=(1, 1))  # Yellow piece (large)
        self.game.make_move(piece_idx=1, to_pos=(0, 1))  # Red piece (medium)
        self.game.make_move(piece_idx=1, to_pos=(1, 0))  # Yellow piece (medium)
        self.game.make_move(piece_idx=2, to_pos=(0, 2))  # Red piece (small)

        result = self.game.make_move(piece_idx=2, to_pos=(1, 2))  # Yellow piece (medium)
        self.assertFalse(result)    # ensure the move was not made
        
        # At this point, Red should win
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "red")
    
    def test_expose_opponent_win(self):
        """Test that moving a piece that exposes a winning sequence for opponent results in opponent win."""
        # Set up a scenario where moving a piece would expose opponent's win
        
        # Place three yellow pieces in a row with one covered by red
        self.game.make_move(piece_idx=0, to_pos=(0, 0))  # Red piece (large)
        self.game.make_move(piece_idx=0, to_pos=(1, 1))  # Yellow piece (large)

        self.game.make_move(piece_idx=1, to_pos=(0, 2))  # Red piece (medium)
        self.game.make_move(piece_idx=0, to_pos=(0, 2))  # Yellow piece, gobbles (large)
        # self.game.make_move(from_pos=(1, 1), to_pos=(0, 2))  # Placed yellow piece (large)
        
        self.game.make_move(piece_idx=0, to_pos=(0, 1))  # Red piece (large)
        self.game.make_move(from_pos=(0, 2), to_pos=(1, 2))  # Placed yellow piece, initially gobbled red medium (large)
        
        # At this point, Red should win
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "red")
    
    def test_expose_opponent_win_self_win(self):
        """Test that moving a piece that exposes a winning sequence for opponent results in opponent win."""
        # Set up a scenario where moving a piece would expose opponent's win
        
        # Place three yellow pieces in a row with one covered by red
        self.game.make_move(piece_idx=0, to_pos=(0, 0))  # Red piece (large)
        self.game.make_move(piece_idx=0, to_pos=(1, 1))  # Yellow piece (large)

        self.game.make_move(piece_idx=1, to_pos=(0, 2))  # Red piece (medium)
        self.game.make_move(piece_idx=0, to_pos=(0, 2))  # Yellow piece, gobbles (large)
        # self.game.make_move(from_pos=(1, 1), to_pos=(0, 2))  # Placed yellow piece (large), cud use this as well
        
        self.game.make_move(piece_idx=0, to_pos=(0, 1))  # Red piece (large)
        self.game.make_move(piece_idx=0, to_pos=(1, 0))  # Yellow piece (medium rn)
        
        self.game.make_move(piece_idx=1, to_pos=(2, 0))  # Red piece (small)
        self.game.make_move(from_pos=(0, 2), to_pos=(1, 2))  # Placed yellow piece, initially gobbled red medium (large)
                                                            # Yellow has 3 in a row if this placed in (1, 2), but shouldn't win
        
        # At this point, Red should win
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "red")
    
    def test_rewind(self):
        """Test rewinding moves."""
        # Make some moves
        self.game.make_move(piece_idx=0, to_pos=(0, 0))  # Red piece
        self.game.make_move(piece_idx=0, to_pos=(1, 1))  # Yellow piece
        
        # Rewind one move
        self.game.rewind()
        
        # Should be yellow's turn again and the piece should be gone
        self.assertEqual(self.game.current_player.color, "yellow")
        self.assertIsNone(self.game.board.grid[1][1])
        
        # Rewind another move
        self.game.rewind()
        
        # Should be red's turn again and the piece should be gone
        self.assertEqual(self.game.current_player.color, "red")
        self.assertIsNone(self.game.board.grid[0][0])
    
    def test_nested_gobbling(self):
        """Test gobbling a piece that has already gobbled another piece."""
        # Place a small red piece
        self.game.make_move(piece_idx=4, to_pos=(0, 0))
        
        # Place a medium yellow piece on top of it
        self.game.make_move(piece_idx=2, to_pos=(0, 0))
        
        # Place a large red piece on top of both
        self.game.make_move(piece_idx=0, to_pos=(0, 0))
        
        # Switch manually to red and move the large red piece away
        self.game.switch_player()
        self.game.make_move(from_pos=(0, 0), to_pos=(1, 1))
        
        # Check that the medium yellow piece is revealed
        self.assertIsNotNone(self.game.board.grid[0][0])
        self.assertEqual(self.game.board.grid[0][0].color, "yellow")
        self.assertEqual(self.game.board.grid[0][0].size, Size.MEDIUM)
        
        # Move the medium yellow piece away. Note, it is yellow's chance now.
        self.game.make_move(from_pos=(0, 0), to_pos=(2, 2))
        
        # Check that the small red piece is revealed
        self.assertIsNotNone(self.game.board.grid[0][0])
        self.assertEqual(self.game.board.grid[0][0].color, "red")
        self.assertEqual(self.game.board.grid[0][0].size, Size.SMALL)

    def test_game_over_state(self):
        """Test that no moves are allowed after game is over."""
        # Create a winning state
        self.game.make_move(piece_idx=0, to_pos=(0, 0))
        self.game.make_move(piece_idx=0, to_pos=(1, 0))
        self.game.make_move(piece_idx=1, to_pos=(0, 1))
        self.game.make_move(piece_idx=1, to_pos=(1, 1))
        self.game.make_move(piece_idx=2, to_pos=(0, 2))
        
        # Game should be over with red as winner
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "red")
        
        # Try to make another move (should fail)
        result = self.game.make_move(piece_idx=2, to_pos=(1, 2))
        self.assertFalse(result)
        
        # Try to switch players (should not affect game state)
        current_winner = self.game.winner
        self.game.switch_player()
        self.assertEqual(self.game.winner, current_winner)
        self.assertTrue(self.game.game_over)

    def test_multiple_winning_lines(self):
        """Test creating multiple winning alignments with a single move."""
        # Setup a position where placing a piece creates two winning lines
        self.game.make_move(piece_idx=0, to_pos=(0, 0)) # Red large, top-left
        self.game.make_move(piece_idx=0, to_pos=(1, 0)) # Yellow large, middle-left

        self.game.make_move(piece_idx=1, to_pos=(1, 1)) # Red medium, centre
        self.game.make_move(piece_idx=1, to_pos=(0, 1)) # Yellow medium, top-centre
        
        self.game.make_move(piece_idx=0, to_pos=(1, 2)) # Red large, middle-right
        self.game.make_move(piece_idx=0, to_pos=(2, 0)) # Yellow large, bottom-left
        
        self.game.make_move(piece_idx=1, to_pos=(0, 2)) # Red small, top-right
        self.game.make_move(piece_idx=2, to_pos=(2, 1)) # Yellow small, bottom-centre
        
        # Place piece to create two winning lines (diagonal and right column)
        self.game.make_move(piece_idx=0, to_pos=(2, 2)) # Red medium, bottom-right
                                                        # there's a small red remaining now
        
        # Game should be over with red as winner
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "red")

if __name__ == '__main__':
    unittest.main()