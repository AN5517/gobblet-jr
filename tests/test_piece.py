import unittest
from src.game.piece import Piece, Size

class TestPiece(unittest.TestCase):
    """Test cases for the Piece class."""

    def test_init(self):
        """Test piece initialization."""
        piece = Piece(Size.LARGE, "red")
        self.assertEqual(piece.color, "red")
        self.assertEqual(piece.size, Size.LARGE)
        self.assertIsNone(piece.gobbled_piece)
    
    def test_can_gobble(self):
        """Test if a piece can gobble another piece."""
        large_piece = Piece(Size.LARGE, "red")
        medium_piece = Piece(Size.MEDIUM, "yellow")
        small_piece = Piece(Size.SMALL, "red")
        
        # A larger piece can gobble a smaller piece
        self.assertTrue(large_piece.can_gobble(medium_piece))
        self.assertTrue(large_piece.can_gobble(small_piece))
        self.assertTrue(medium_piece.can_gobble(small_piece))
        
        # A piece cannot gobble a piece of the same size
        same_size_piece = Piece(Size.LARGE, "yellow")
        self.assertFalse(large_piece.can_gobble(same_size_piece))
        
        # A piece cannot gobble a larger piece
        self.assertFalse(small_piece.can_gobble(medium_piece))
        self.assertFalse(medium_piece.can_gobble(large_piece))
        self.assertFalse(small_piece.can_gobble(large_piece))
        
    def test_gobble_and_reveal(self):
        """Test gobbling and revealing pieces."""
        large_piece = Piece(Size.LARGE, "red")
        small_piece = Piece(Size.SMALL, "yellow")
        
        # Test gobbling
        large_piece.gobble(small_piece)
        self.assertEqual(large_piece.gobbled_piece, small_piece)
        
        # Test revealing
        revealed = large_piece.reveal()
        self.assertEqual(revealed, small_piece)
        self.assertIsNone(large_piece.gobbled_piece)

if __name__ == '__main__':
    unittest.main()