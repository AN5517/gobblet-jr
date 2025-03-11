import unittest
from src.game.board import Board
from src.game.piece import Piece, Size

class TestBoard(unittest.TestCase):
    """Test cases for the Board class."""

    def setUp(self):
        """Set up a new board before each test."""
        self.board = Board()
    
    def test_init(self):
        """Test board initialization."""
        self.assertEqual(len(self.board.grid), 3)
        self.assertEqual(len(self.board.grid[0]), 3)
        
        # All positions should be empty initially
        for row in self.board.grid:
            for cell in row:
                self.assertIsNone(cell)
    
    def test_place_piece(self):
        """Test placing a piece on the board."""
        piece = Piece(Size.LARGE, "red")
        
        # Place on empty cell
        result = self.board.place_piece(piece, 0, 0)
        self.assertTrue(result)
        self.assertEqual(self.board.grid[0][0], piece)
        
        # Try placing a smaller piece on top (should fail)
        small_piece = Piece(Size.SMALL, "yellow")
        result = self.board.place_piece(small_piece, 0, 0)
        self.assertFalse(result)
        self.assertEqual(self.board.grid[0][0], piece)  # Original piece still there
        
        # Try placing a larger piece on top (should succeed)
        huge_piece = Piece(42, "yellow")  # Using a custom size larger than standard
        result = self.board.place_piece(huge_piece, 0, 0)
        self.assertTrue(result)
        self.assertEqual(self.board.grid[0][0], huge_piece)
    
    def test_move_piece(self):
        """Test moving a piece on the board."""
        piece = Piece(Size.MEDIUM, "red")
        
        # Place piece
        self.board.place_piece(piece, 0, 0)
        
        # Move to empty cell
        result = self.board.move_piece(0, 0, 1, 1)
        self.assertTrue(result)
        self.assertIsNone(self.board.grid[0][0])
        self.assertEqual(self.board.grid[1][1], piece)
        
        # Try moving from empty cell (should fail)
        result = self.board.move_piece(0, 0, 2, 2)
        self.assertFalse(result)
        
        # Try moving to same cell (should fail)
        result = self.board.move_piece(1, 1, 1, 1)
        self.assertFalse(result)
        
    def test_gobbling_mechanics(self):
        """Test gobbling mechanics when moving pieces."""
        small_piece = Piece(Size.SMALL, "red")
        medium_piece = Piece(Size.MEDIUM, "yellow")
        
        # Place pieces
        self.board.place_piece(small_piece, 0, 0)
        self.board.place_piece(medium_piece, 1, 1)
        
        # Move medium piece to gobble small piece
        result = self.board.move_piece(1, 1, 0, 0)
        print("Medium piece at 1, 1 moved to 0, 0")
        self.assertTrue(result)
        self.assertEqual(self.board.grid[0][0], medium_piece)
        
        # Test gobbling directly
        test_small = Piece(Size.SMALL, "red")
        test_medium = Piece(Size.MEDIUM, "yellow")
        test_medium.gobble(test_small)
        self.assertEqual(test_medium.gobbled_piece, test_small)
        
        # Move medium piece away - should reveal small piece
        result = self.board.move_piece(0, 0, 2, 2)
        self.assertTrue(result)
        print("Piece at 0, 0 moved to 2, 2")
        self.assertEqual(self.board.grid[2][2], medium_piece)
        self.assertEqual(self.board.grid[0][0], small_piece)
        print("Both 0, 0 and 2, 2 have the correct pieces")
        self.assertIsNone(medium_piece.gobbled_piece)
        print("Medium piece no longer has a gobbled piece")
    
    def test_check_winner(self):
        """Test checking for a winner."""
        # No winner initially
        self.assertIsNone(self.board.check_winner())
        
        # Create a horizontal win for red
        for col in range(3):
            piece = Piece(Size.MEDIUM, "red")
            self.board.place_piece(piece, 0, col)
        
        self.assertEqual(self.board.check_winner(), "red")
        
        # Reset and create a vertical win for yellow
        self.board = Board()
        for row in range(3):
            piece = Piece(Size.LARGE, "yellow")
            self.board.place_piece(piece, row, 0)
        
        self.assertEqual(self.board.check_winner(), "yellow")
        
        # Reset and create a diagonal win for red
        self.board = Board()
        for i in range(3):
            piece = Piece(Size.SMALL, "red")
            self.board.place_piece(piece, i, i)
        
        self.assertEqual(self.board.check_winner(), "red")

if __name__ == '__main__':
    unittest.main()