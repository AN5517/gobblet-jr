from .piece import Piece, Size

class Player:
    """Represents a player in Gobblet Jr."""
    
    def __init__(self, color):
        """
        Args:
            color (str): Player color ('red' or 'yellow')
        """
        self.color = color
        # Each player starts with 6 pieces: 2 large, 2 medium, 2 small
        self.pieces = [
            Piece(Size.LARGE, color), Piece(Size.LARGE, color),  # Large pieces
            Piece(Size.MEDIUM, color), Piece(Size.MEDIUM, color),  # Medium pieces
            Piece(Size.SMALL, color), Piece(Size.SMALL, color)   # Small pieces
        ]
        self.board_pieces = []
    
    def get_available_pieces(self):
        """
        Get pieces not yet placed on the board.
        
        Returns:
            list: List of available pieces
        """
        return self.pieces
    
    def place_piece(self, piece_index):
        """
        Args:
            piece_index (int): Index of the piece to place
            
        Returns:
            Piece: The piece being placed
        """
        piece = self.pieces.pop(piece_index)
        self.board_pieces.append(piece)
        return piece
    
    def return_piece(self, piece):
        """
        Return a piece to the player's available pieces.
        
        Args:
            piece (Piece): The piece to return
        """
        self.pieces.append(piece)
        if piece in self.board_pieces:
            self.board_pieces.remove(piece)