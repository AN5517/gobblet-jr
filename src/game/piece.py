class Size:
    """Piece sizes"""
    SMALL = 0
    MEDIUM = 1
    LARGE = 2

class Piece:
    """Represents a game piece"""
    
    def __init__(self, size, color):
        """
        Args:
            size (int): Size of piece (0=small, 1=medium, 2=large)
            color (str): Color of the piece ('red' or 'yellow')
        """
        self.size = size
        self.color = color
        self.gobbled_piece = None
    
    def can_gobble(self, other_piece):
        """
        Check if this piece can gobble another piece.
        
        Args:
            other_piece (Piece or None): Piece to potentially gobble
            
        Returns:
            bool: True if this piece can gobble the other piece
        """
        if other_piece is None:
            return True
        return self.size > other_piece.size
    
    def gobble(self, other_piece):
        """
        Gobble another piece.
        
        Args:
            other_piece (Piece): Piece to gobble
        """
        self.gobbled_piece = other_piece
    
    def reveal(self):
        """
        Reveal the piece that was gobbled by this piece.
        
        Returns:
            Piece or None: The piece that was gobbled, or None
        """
        revealed = self.gobbled_piece
        self.gobbled_piece = None
        return revealed