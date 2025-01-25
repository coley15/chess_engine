import pygame
import random
import time

pygame.mixer.init()

# Constants
ROWS = 8
COLS = 8
TILE_SIZE = 100
WIDTH, HEIGHT = ROWS * TILE_SIZE, COLS * TILE_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Sound effects
capture_sound = pygame.mixer.Sound("sfx/capture.mp3")
move_sound = pygame.mixer.Sound('sfx/move.mp3')

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

    def get_valid_moves(self, board):
        y, x = self.position
        valid_moves = []

        # If you reach the end of the board just instantly return no moves
        # Todo definently add queen promotion if this is the case instead of
        # Just returning an empty array

        # If the pawn isn't at the very end, proceed
        if self.colour == 'white':
            # One square forward
            if y > 0 and board[y - 1][x] is None:
                valid_moves.append((y - 1, x))

            # Two squares forward only if it's your first move
            if y == 6 and board[y - 2][x] is None and board[y - 1][x] is None:
                valid_moves.append((y - 2, x))

            # Diagonal capture: top-left:
            if x > 0 and board[y - 1][x - 1] is not None and board[y - 1][x - 1].colour != self.colour:
                valid_moves.append((y - 1, x - 1))
            
            # Diagonal capture: top-right:
            if x < COLS - 1 and board[y - 1][x + 1] is not None and board[y - 1][x + 1].colour != self.colour:
                valid_moves.append((y - 1, x + 1))
               
        elif self.colour == 'black':
            # Moving normally, one square aslong as the square in-front is None (empty)
            if y < 7 and board[y + 1][x] is None:
                valid_moves.append((y + 1, x))

            # Moving two squares on the first turn
            if y == 1 and board[y + 2][x] is None and board[y + 1][x] is None:
                valid_moves.append((y + 2, x))

            # Diagonal capture: Check bottom-left
            if x > 0 and board[y + 1][x - 1] is not None and board[y + 1][x - 1].colour != self.colour:
                valid_moves.append((y + 1, x - 1))

            # Diagonal capture: Check bottom-right
            if x < COLS - 1 and board[y + 1][x + 1] is not None and board[y + 1][x + 1].colour != self.colour:
                valid_moves.append((y + 1, x + 1))

        return valid_moves


class Knight:
    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.is_highlighted = False
        # All possible L-shape patterns offsets
        self.moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        if self.colour == 'black':
            self.image = pygame.image.load('assets\\bN.png')
        else:
            self.image = pygame.image.load('assets\\wN.png')

    def get_valid_moves(self, board):
        y, x = self.position

        valid_moves = []

        for dy, dx in self.moves:
            # Create a new y and x value using the L-shape offsets
            new_y, new_x = y + dy, x + dx

            # Ensure the new position is in-bounds
            if 0 <= new_y < 8 and 0 <= new_x < 8:
                target = board[new_y][new_x]

                # If the target landing spot is empty or is of another player colour, then it is valid
                if target is None or target.colour != self.colour:
                    valid_moves.append((new_y, new_x))

        return valid_moves

class Bishop:
    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.is_highlighted = False

        if self.colour == 'black':
            self.image = pygame.image.load('assets\\bB.png')
        else:
            self.image = pygame.image.load('assets\\wB.png')

    def get_valid_moves(self, board):
        valid_moves = []
        y, x = self.position
        
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dy, dx in directions:
            i, j = y, x

            while True:
                i += dy
                j += dx

                if 0 <= i < ROWS and 0 <= j < COLS:
                    piece = board[i][j]
                    if piece is None:
                        valid_moves.append((i, j))

                    elif piece.colour != self.colour:
                        valid_moves.append((i, j))

                        break
                
                    else:
                        break
                
                else:
                    break
            
        return valid_moves


class Rook:
    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.is_highlighted = False
        self.has_moved = False

        if self.colour == 'black':
            self.image = pygame.image.load('assets\\bR.png')
        else:
            self.image = pygame.image.load('assets\\wR.png')

    def get_valid_moves(self, board):
        valid_moves = []
        y, x = self.position

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dy, dx in directions:
            i, j = y, x

            while True:
                i += dy
                j += dx

                if 0 <= i < ROWS and 0 <= j < COLS:
                    piece = board[i][j]
                    if piece is None:
                        valid_moves.append((i, j))

                    elif piece.colour != self.colour:
                        valid_moves.append((i, j))

                        break

                    else:
                        break
                else:
                    break
            

        return valid_moves

class Queen:
    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.is_highlighted = False

        if self.colour == 'black':
            self.image = pygame.image.load('assets\\bQ.png')
        else:
            self.image = pygame.image.load('assets\\wQ.png')

    def get_valid_moves(self, board):
        valid_moves = []
        y, x = self.position

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dy, dx in directions:
            i, j = y, x

            while True:
                i += dy
                j += dx

                if 0 <= i < ROWS and 0 <= j < COLS:
                    piece = board[i][j]
                    if piece is None:
                        valid_moves.append((i, j))

                    elif piece.colour != self.colour:
                        valid_moves.append((i, j))

                        break
                    else:
                        break
                else:
                    break
        
        return valid_moves

class King:
    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.is_highlighted = False
        self.has_moved = False

        if self.colour == 'black':
            self.image = pygame.image.load('assets\\bK.png')
        else:
            self.image = pygame.image.load('assets\\wK.png')

    def get_valid_moves(self, board):
        valid_moves = []
        y, x = self.position

        # Normal king movement
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dy, dx in directions:
            new_y, new_x = y + dy, x + dx

            if 0 <= new_y < ROWS and 0 <= new_x < COLS:
                target = board[new_y][new_x]

                if target is None or target.colour != self.colour:
                    valid_moves.append((new_y, new_x))

        # Castling logic
        if not self.has_moved: # Check if the King hasn't moved
            row = self.position[0]

            # Kingside castling
            kingside_rook = board[row][7]
            # Check if the kingside rook is actually there and if it has moved before
            if isinstance(kingside_rook, Rook) and not kingside_rook.has_moved:
                if board[row][5] is None and board[row][6] is None: # The squares between the king and the rook must be None
                    if not game.is_square_under_attack((row, 4), self.colour) and \
                    not game.is_square_under_attack((row , 5), self.colour) and \
                    not game.is_square_under_attack((row, 6), self.colour):
                        valid_moves.append((row, 6))

            # Queen side castling
            queenside_rook = board[row][0]
            if isinstance(queenside_rook, Rook) and not queenside_rook.has_moved:
                if board[row][3] is None and board[row][2] is None and board[row][1] is None:  # Squares are empty
                    if not game.is_square_under_attack((row, 4), self.colour) and \
                    not game.is_square_under_attack((row, 3), self.colour) and \
                    not game.is_square_under_attack((row, 2), self.colour):
                        valid_moves.append((row, 2))  # Castling move (queenside)



        return valid_moves

# Define inital board state using cardnality operators
board = [
    [Rook('black', (0, 0)), Knight('black', (0, 1)), Bishop('black', (0, 2)), Queen('black', (0, 3)), King('black', (0, 4)), Bishop('black', (0, 5)), Knight('black', (0, 6)), Rook('black', (0, 7))],
    [Pawn('black', (1, x)) for x in range(COLS)],
    [None] * COLS,
    [None] * COLS,
    [None] * COLS,
    [None] * COLS,
    [Pawn('white', (6, x)) for x in range(COLS)],
    [Rook('white', (7, 0)), Knight('white', (7, 1)), Bishop('white', (7, 2)), Queen('white', (7, 3)), King('white', (7, 4)), Bishop('white', (7, 5)), Knight('white', (7, 6)), Rook('white', (7, 7))]
]



class Board:
    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        self.tile_size = TILE_SIZE
        self.board = board
        self.nodes_evaluated = 0


    def draw(self, valid_moves):
        
        # Draw board
        for row in range(self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(WIN, (37, 150, 190), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(WIN, (240, 217, 181), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))


        # Loop through every piece and check if it is highlighted, if it is draw a red tile
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != None and self.board[row][col].is_highlighted:
                    pygame.draw.rect(WIN, (255, 40, 40), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))

        # Highlight valid moves
        for move in valid_moves:
            pygame.draw.rect(WIN, (0, 255, 0), (move[1] * self.tile_size, move[0] * self.tile_size, self.tile_size, self.tile_size))

        # Draw pieces
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.board[row][col]
                if piece:
                    image = pygame.transform.scale(piece.image, (self.tile_size, self.tile_size))
                    WIN.blit(image, (col * self.tile_size, row * self.tile_size))
        

class Game:
    def __init__(self, board):
        self.board = board.board
        self.selected_piece = None
        self.turn = 'white'
        self.valid_moves = []
        self.game_over = False
        self.pruned_branches = 0
        self.transposition_table = {}

    def handle_press(self, row, col):

        piece = self.board[row][col]

        # If the game is over stop processing inputs
        if self.game_over == True:
            return

        # If a piece has already been selected (i.e second click)
        if self.selected_piece is not None:
            
            # Check if the user clicked the same piece twice to de-select it
            if self.selected_piece == piece:
                self.selected_piece.is_highlighted = False
                self.selected_piece = None
                self.valid_moves = []
        
            # If the user clicked onto an empty square for their second click
            else:
                # Check if the place the player wants to move is in the valid move list
                if (row, col) in self.valid_moves:
                    # (row, col) in this case is the square the selected piece is moving to
                    self.move_piece(self.selected_piece, row, col)
                    self.switch_turn()

                    if self.check_insufficent_material():
                        print("Draw by insufficent material!")

                        self.game_over = True

                    if self.is_checkmate():
                        print(f"Checkmate! {self.turn.capitalize()} loses.")

                        self.game_over = True

                    # Remove highlight attribute and return selected_piece to None
                    self.selected_piece.is_highlighted = False
                    self.selected_piece = None
                    self.valid_moves = []

        # If a piece hasn't been selected yet (i.e first click)
        else:
            if piece and self.turn == piece.colour:
                self.selected_piece = piece
                self.selected_piece.is_highlighted = True
                self.valid_moves = self.get_valid_moves(self.selected_piece)

    def move_piece(self, piece, row, col, simulation=False):
        
        # Get the positon of the piece before it moves
        old_row, old_col = piece.position

        # Checks if the piece being moved is the king and if it's moving two squares horizontally
        # This means you know it's a castling move so now adjust the rook
        # Also ensure that simulation is set to False
        if isinstance(piece, King) and abs(col - old_col) == 2 and not simulation:
            # Kingside castling
            if col > old_col:
                # Just swap the rook to the right spot and update it position
                rook = self.board[old_row][7]
                self.board[old_row][7] = None
                self.board[old_row][col - 1] = rook
                rook.position = (old_row, col - 1)

            # Queenside castling
            else:
                # Same thing here, just swap the rook to where it needs to be
                rook = self.board[old_row][0]
                self.board[old_row][0] = None
                self.board[old_row][col + 1] = rook
                rook.position = (old_row, col + 1)


        # If the piece moving is a king or a rook update its has_moved variable
        if not simulation and isinstance(piece, (Rook, King)):
            piece.has_moved = True


        # Prioritize playing the capture sound over the move sound
        captured_piece = self.board[row][col]
        if captured_piece and self.turn == 'white':
            pygame.mixer.Sound.play(capture_sound)

        # Noone tryna hear blacks 1000 different routes in sfx
        elif captured_piece is None and self.turn == 'white':
            pygame.mixer.Sound.play(move_sound)

        # Replace that position with None
        self.board[old_row][old_col] = None
        # Now update the new row, col with the piece
        self.board[row][col] = piece

        # Update the piece position, this is extremely important as the old_row, old_col would be outdated
        # When replacing with none
        piece.position = (row, col)

        # If the newly moved piece was a pawn and can promote, promote it to a queen automatically
        if isinstance(piece, Pawn):
            if piece.colour == 'white' and row == 0:
                self.promote_pawn(piece)
            elif piece.colour == 'black' and row == 7:
                self.promote_pawn(piece)


    def switch_turn(self):
        self.turn = 'black' if self.turn == 'white' else 'white'

        if self.is_stalemate():
            print(f"Stalemate! {self.turn.capitalize()} has no valid moves and is not in check.")
            self.game_over = True


    def get_valid_moves(self, selected_piece):
        all_valid_moves = selected_piece.get_valid_moves(self.board)
        safe_moves = []

        if not selected_piece:
            return []

        # Only return moves that do not violate moving into check rules
        for move in all_valid_moves:
            if not self.exposes_king(selected_piece, move):
                safe_moves.append(move)


        return safe_moves

    # Basically checks if making a certain move will cause the king to be in check
    def exposes_king(self, selected_piece, move):
        old_row, old_col = selected_piece.position
        new_row, new_col = move

        # Simulate the move
        orignal_piece = self.board[new_row][new_col]
        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = selected_piece
        selected_piece.position = (new_row, new_col)

        # Find the colour of the king of the corresponding turn and 
        # Then see if it's under attack after this 'simulated' move
        king_position = self.find_king(self.turn)
        in_check = self.is_square_under_attack(king_position, self.turn)

        # Return the board pre-simulated move
        self.board[old_row][old_col] = selected_piece
        self.board[new_row][new_col] = orignal_piece
        selected_piece.position = (old_row, old_col)

        # Return if the king is in check after making a certain move
        return in_check

    # Return the (row, col) of the current turns king
    def find_king(self, colour):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and isinstance(piece, King) and piece.colour == colour:
                    return (row, col)
        
        return None

    # The position parameter is the position of the piece you are checking is under attack
    def is_square_under_attack(self, position, colour):
        opponent_colour = 'black' if colour == 'white' else 'white'
        row, col = position

        # Loop through the whole board for the opponents coloured pieces
        # Then find their valid moves, if the king is in that position, then it's in check
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board[r][c]
                if piece and piece.colour == opponent_colour:
                    if isinstance(piece, King):
                        king_moves = [
                            (r + dr, c + dc)
                            for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                            if 0 <= r + dr < ROWS and 0 <= c + dc < COLS
                        ]
                        if position in king_moves:
                            return True
                    else:
                        # For all other pieces use their valid moves
                        if position in piece.get_valid_moves(self.board):
                            return True

        return False

    def is_checkmate(self):
        king_position = self.find_king(self.turn)

        # No king ?
        if not king_position:
            return False

        # Check if the king is currently under attack
        if self.is_square_under_attack(king_position, self.turn):
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.board[row][col]
                    if piece and piece.colour == self.turn:
                        # Check if it's possible to use one of your own
                        # Pieces to block a checkmate or to take the attacker
                        valid_moves = piece.get_valid_moves(self.board)
                        for move in valid_moves:
                            if not self.exposes_king(piece, move):
                                return False

            print("Checkmate!")
            return True
        
        return False

    def is_stalemate(self):
        king_position = self.find_king(self.turn)

        if not king_position:
            return False

        # If the king is not under attack
        if not self.is_square_under_attack(king_position, self.turn):
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.board[row][col]
                    if piece and piece.colour == self.turn:
                        # Go through all of your own pieces and see if you have any move
                        # Possibilites (calling self.expose_king(piece, move) ensures you don't make any moves into checks)
                        # If you have valid moves return False
                        valid_moves = piece.get_valid_moves(self.board)
                        for move in valid_moves:
                            if not self.exposes_king(piece, move):
                                return False
            print("Stalemate")
            return True
        
        return False
        
    def promote_pawn(self, pawn):
        promoted_piece = Queen(pawn.colour, (pawn.position))

        row, col = pawn.position
        self.board[row][col] = promoted_piece


    def check_insufficent_material(self):
        # King vs. King
        # King vs. Bishop and King
        # King vs. Knight and King
        black_pieces = [piece for row in self.board for piece in row if piece and piece.colour == 'black']
        white_pieces = [piece for row in self.board for piece in row if piece and piece.colour == 'white']

        white_piece_count = len(white_pieces)
        black_piece_count = len(black_pieces)

        total_count = white_piece_count + black_piece_count

        # Two kings situation
        if total_count == 2:
            return True
        
        # Three pieces; check if one of their pieces is a bishop or a knight
        elif total_count == 3:
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.board[row][col] 
                    if piece and isinstance(piece, Knight) or isinstance(piece, Bishop):
                        return True


    def simulate_move(self, piece, move):
        """ Simulate moving a piece """
        old_pos = piece.position
        captured_piece = self.board[move[0]][move[1]]

        self.board[old_pos[0]][old_pos[1]] = None
        self.board[move[0]][move[1]] = piece
        piece.position = move

        return old_pos, captured_piece
    
    def undo_move(self, piece, old_position, move, captured_piece):
        """ Undo a simulated move """
        piece.position = old_position
        self.board[old_position[0]][old_position[1]] = piece
        self.board[move[0]][move[1]] = captured_piece

    def get_all_pieces(self, colour):
        # Return all the pieces of a certain colour
        return [piece for row in self.board for piece in row if piece and piece.colour == colour]


    def count_moves_at_ply(self, depth):

        if depth == 0:
            return 1

        total_moves = 0

        for piece in self.get_all_pieces(self.turn):
            for move in self.get_valid_moves(piece):
                old_pos, captured_piece = self.simulate_move(piece, move)
                self.switch_turn()
                total_moves += self.count_moves_at_ply(depth - 1)
                self.switch_turn()
                self.undo_move(piece, old_pos, move, captured_piece)

        
        return total_moves


    def ai_move(self):
        pass



board = Board()
game = Game(board)

ai_turn_start_time = None
# A fabricated time it takes for the ai to make a move
# Possibly remove this later as it may cause problems
# ALso it's in seconds
fake_ai_time = 0.0
clock = pygame.time.Clock()

run = True
while run:

    clock.tick(300)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row, col = y // TILE_SIZE, x // TILE_SIZE

            game.handle_press(row, col)

    depth = 3

    start_time = time.time()
    print(f"At depth {depth}, total moves = {game.count_moves_at_ply(depth)}")

    print(f"Execution time: {time.time() - start_time:.2f} seconds")
    # Add (or remove) "and game.turn == 'black'" if you want only black to play as an "AI"
    #if game.turn == 'black' and not game.game_over:
        #game.ai_move()


    board.draw(game.valid_moves)

    pygame.display.update()
    pygame.display.set_caption("Chess")



# Todo

# Add commenting
# Fix the alpha-beta pruning as I have a feeling that it isn't actually working at all
# Improve more early game moves, it struggles with devloping central pawns
# 1. Add alpha-beta pruning
# isinstance


# Check if the same move is being tested twice like in the alpha beta pruning just print the move fully 

