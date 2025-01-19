import pygame

ROWS = 8
COLS = 8
TILE_SIZE = 100
WIDTH, HEIGHT = ROWS * TILE_SIZE, COLS * TILE_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Define classes for all the pieces
class Pawn:
    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.is_highlighted = False

        if self.colour == 'black':
            self.image = pygame.image.load('assets\\bP.png')
        else:
            self.image = pygame.image.load('assets\\wP.png')

class Knight:
    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.is_highlighted = False

        if self.colour == 'black':
            self.image = pygame.image.load('assets\\bN.png')
        else:
            self.image = pygame.image.load('assets\\wN.png')

class Bishop:
    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.is_highlighted = False

        if self.colour == 'black':
            self.image = pygame.image.load('assets\\bB.png')
        else:
            self.image = pygame.image.load('assets\\wB.png')

class Rook:
    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.is_highlighted = False

        if self.colour == 'black':
            self.image = pygame.image.load('assets\\bR.png')
        else:
            self.image = pygame.image.load('assets\\wR.png')

class Queen:
    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.is_highlighted = False

        if self.colour == 'black':
            self.image = pygame.image.load('assets\\bQ.png')
        else:
            self.image = pygame.image.load('assets\\wQ.png')

class King:
    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.is_highlighted = False

        if self.colour == 'black':
            self.image = pygame.image.load('assets\\bK.png')
        else:
            self.image = pygame.image.load('assets\\wK.png')


# Define inital board state using cardnality operators
board = [

    [Rook('black', (0, 0)), Knight('black', (1, 0)), Bishop('black', (2, 0)), Queen('black', (3, 0)), King('black', (4, 0)), Bishop('black', (5, 0)), Knight('black', (6, 0)), Rook('black', (7, 0))],
    [Pawn('black', (0, 1)), Pawn('black', (1, 1)), Pawn('black', (2, 1)), Pawn('black', (3, 1)), Pawn('black', (4, 1)), Pawn('black', (5, 1)), Pawn('black', (6, 1)), Pawn('black', (7, 1))],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [Pawn('white', (0, 6)), Pawn('white', (1, 6)), Pawn('white', (2, 6)), Pawn('white', (3, 6)), Pawn('white', (4, 6)), Pawn('white', (5, 6)), Pawn('white', (6, 6)), Pawn('white', (7, 6))],
    [Rook('white', (0, 7)), Knight('white', (1, 7)), Bishop('white', (2, 7)), Queen('white', (3, 7)), King('white', (4, 7)), Bishop('white', (5, 7)), Knight('white', (6, 7)), Rook('white', (7, 7))],

]


class Board:
    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        self.tile_size = TILE_SIZE
        self.board = board


    def draw(self):
        # Draw board
        for col in range(8):
            for row in range(8):
                if (col + row) % 2 == 0:
                    pygame.draw.rect(WIN, (37, 150, 190), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(WIN, (240, 217, 181), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))


        # Loop through every piece and check if it is highlighted, if it is draw a red tile
        for col in range(8):
            for row in range(8):
                if self.board[col][row] != None and self.board[col][row].is_highlighted:
                    pygame.draw.rect(WIN, (255, 40, 40), (row * self.tile_size, col * self.tile_size, self.tile_size, self.tile_size))


        # Draw pieces
        for col in range(8):
            for row in range(8):
                if self.board[col][row]:
                    # Get the image and position stored within the piece
                    image = self.board[col][row].image
                    pos = self.board[col][row].position

                    # Rescale the image to fit a tile
                    image = pygame.transform.scale(image, (self.tile_size, self.tile_size))
                    WIN.blit(image, (row * self.tile_size, col * self.tile_size))
        


class Game:
    def __init__(self, board):
        self.board = board.board
        self.selected_piece = None
        self.turn = 'white'

    def handle_press(self, col, row):

        piece = self.board[col][row]

        # If a piece has already been selected (i.e second click)
        if self.selected_piece is not None:
            
            # Check if the user clicked the same piece twice to de-select it
            if self.selected_piece == piece:
                self.selected_piece.is_highlighted = False
                self.selected_piece = None
        
            # If the user clicked onto an empty square for their second click
            else: 
                self.move_piece(self.selected_piece, row, col)
                self.switch_turn()

                # Remove highlight attribute and return selected_piece to None
                self.selected_piece.is_highlighted = False
                self.selected_piece = None

        # If a piece hasn't been selected yet (i.e first click)
        else:
            if piece and self.turn == piece.colour:
                self.selected_piece = piece
                self.selected_piece.is_highlighted = True

    def move_piece(self, piece, col, row):
        
        # Get the positon of the piece before it moves
        old_col, old_row = piece.position
        # Replace that position with None
        self.board[old_row][old_col] = None
        # Now update the new row, col with the piece
        self.board[row][col] = piece

        # Update the piece position, this is extremely important as the old_row, old_col would be outdated
        # When replacing with none
        piece.position = (col, row)


    def switch_turn(self):
        self.turn = 'black' if self.turn == 'white' else 'white'


board = Board()
game = Game(board)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row, col = x // TILE_SIZE, y // TILE_SIZE

            game.handle_press(col, row)


    board.draw()

    pygame.display.update()
    pygame.display.set_caption("Chess")


# Todo

# 1. Ensure that you cannot take your own pieces
# 2. Implement piece movement logic
# 3. Add checkmate, checks, and stalements
# 4. Add alpha-beta pruning
# 5. Stockfish


