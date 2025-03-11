import unittest
from src.game.player import Player
from src.game.piece import Piece, Size

class TestPlayer(unittest.TestCase):
    """Test cases for the Player class."""

    def test_init(self):
        """Test player initialization."""
        player = Player("red")
        self.assertEqual(player.color, "red")
        self.assertEqual(len(player.pieces), 6)  # 2 of each size
        self.assertEqual(len(player.board_pieces), 0)
        
        # Check that pieces are of correct size and color
        sizes = [piece.size for piece in player.pieces]
        colors = [piece.color for piece in player.pieces]
        
        # Should have 2 pieces of each size
        self.assertEqual(sizes.count(Size.SMALL), 2)
        self.assertEqual(sizes.count(Size.MEDIUM), 2)
        self.assertEqual(sizes.count(Size.LARGE), 2)
        
        # All pieces should be the player's color
        for color in colors:
            self.assertEqual(color, "red")
    
    def test_get_available_pieces(self):
        """Test getting available pieces."""
        player = Player("yellow")
        pieces = player.get_available_pieces()
        self.assertEqual(pieces, player.pieces)
        self.assertEqual(len(pieces), 6)
    
    def test_place_piece(self):
        """Test placing a piece."""
        player = Player("red")
        original_count = len(player.pieces)
        
        # Place a piece
        piece = player.place_piece(0)
        
        # Check that piece was moved from available to board pieces
        self.assertEqual(len(player.pieces), original_count - 1)
        self.assertEqual(len(player.board_pieces), 1)
        self.assertIn(piece, player.board_pieces)
    
    def test_return_piece(self):
        """Test returning a piece to the player."""
        player = Player("yellow")
        
        # Place a piece first
        piece = player.place_piece(0)
        original_available_count = len(player.pieces)
        original_board_count = len(player.board_pieces)
        
        # Return the piece
        player.return_piece(piece)
        
        # Check that piece was moved from board to available pieces
        self.assertEqual(len(player.pieces), original_available_count + 1)
        self.assertEqual(len(player.board_pieces), original_board_count - 1)
        self.assertIn(piece, player.pieces)
        self.assertNotIn(piece, player.board_pieces)

if __name__ == '__main__':
    unittest.main()