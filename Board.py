from __future__ import print_function
from pieces import Knight, Queen
from random import choice, sample, shuffle


# Represents the chess board.
class Board:

    """
    Ctor.
    input: Dictionary of chess pieces. For example: {'QUEEN': 2} will randomly locate
    2 queens on the board in 2 different squares.
    """

    def __init__(self, request):
        self.N = 12
        self.__list_of_pieces = []

        # Create a new chess piece instance based on request.
        for (key, value) in (request.items()):
            # Get piece type.
            piece_type = key
            # Iterate until total request number of each chess piece type has been created.
            for _ in range(value):
                new_piece = None
                location = self.random_move()
                if piece_type == 'KNIGHT':
                    new_piece = Knight(location['x'], location['y'])
                elif piece_type == 'QUEEN':
                    new_piece = Queen(location['x'], location['y'])
                # Append new instance to a list.
                self.get_pieces().append(new_piece)

    # Getters.
    def get_pieces(self):
        return self.__list_of_pieces

    def get_size(self):
        return self.N

    # Setter.
    def set_pieces(self, pieces):
        self.__list_of_pieces = pieces

    # Converts (x,y) to a specific square.
    def convert_to_square(self, x, y):
        return y * self.N + x

    # Converts a square to (x,y).
    def convert_to_axis(self, value):
        return {
            'x': value % self.N,
            'y': value / self.N,
        }

    # Returns True if (x,y) is out of the board's boundaries, otherwise False.
    def is_out_of_bound(self, x, y):
        return (x < 0 or x >= self.get_size()) or (y < 0 or y >= self.get_size())

    """
    Checks if a location of a piece overlaps another piece:
    Returns: -1 no overlap- if (x,y) is not in any of current list of piece's location.
              1 there is an overlap- if (x,y) is in one of current list of piece's locations.
    """

    def is_overlap(self, x, y):
        for piece in (self.get_pieces()):
            if (piece.get_x() == x) and (piece.get_y() == y):
                return 1

        return -1

    """
    The function returns a random list of pieces.
    """

    def random_pick(self):
        return sample(self.get_pieces(), len(self.get_pieces()))

    """
    The method gives a random position or a list of a valid position to move.
    Returns dictionary or list:
        if option is False: returns a dictionary of {x, y}.
        if option is True: returns a list of dictionary of {x, y}.
    """

    def random_move(self, option=False):
        # Converts object position to grid system.
        piece_location = []
        for piece in (self.get_pieces()):
            piece_location.append(self.convert_to_square(piece.get_x(), piece.get_y()))
        # Get the last square of the board.
        last_square = self.convert_to_square(self.get_size() - 1, self.get_size() - 1)

        if not option:
            # Choose random square (that doesn't overlap other pieces).
            random_square = choice([i for i in range(0, last_square) if i not in piece_location])
            return self.convert_to_axis(random_square)

        # Get all free squares.
        free_squares = [i for i in range(0, last_square) if i not in piece_location]

        # Shuffle the possible moves.
        shuffle(free_squares)
        possible_moves = []

        # Get all possible moves.
        for val in free_squares:
            possible_moves.append(self.convert_to_axis(val))

        return possible_moves

    """
    Returns the amount of conflicts on the board right now.
    Foreach p in the list of pieces:
            Check how many pieces are in conflicted with p
    The heuristic value: the amount of all conflicts.
    """

    def count_conflicts(self):
        # Set initiate value.
        value = 0

        for piece in (self.get_pieces()):
            for rule in (piece.get_rules()):
                if isinstance(piece, Knight):
                    current_move = rule()
                    if not self.is_out_of_bound(current_move['x'], current_move['y']):
                        inc = self.is_overlap(current_move['x'], current_move['y'])
                        if inc != -1:
                            value += inc
                else:
                    i = 1
                    current_move = rule(i)
                    while not self.is_out_of_bound(current_move['x'], current_move['y']):
                        inc = self.is_overlap(current_move['x'], current_move['y'])
                        if inc != -1:
                            value += inc
                            break
                        i += 1
                        current_move = rule(i)
        return value

    # Calculates the heuristic value of current board's state.
    def calculate_heuristic(self):
        a = self.count_conflicts()

        return {
            'a': a,
            'total': -1 * a,
        }

    # Draws the board (including the pieces).
    def draw(self):
        for y in range(self.get_size() - 1, -1, -1):
            print(str(y) + ' ', end='')
            for x in range(self.get_size()):
                found = False
                for piece in (self.get_pieces()):
                    if piece.get_x() == x and piece.get_y() == y:
                        found = True
                        break
                if found:
                    # print the piece (Q or K).
                    print(' ' + piece.__class__.__name__[0] + ' ', end='')
                else:
                    print(' - ', end='')
            print()

        print("  ", end="")
        for x in range(self.get_size()):
            print(' ' + str(x), end=' ')

        print('\n')

    # Prints the locations of all pieces.
    def print_all_pieces(self):
        for piece in (self.get_pieces()):
            print(str(piece) + ' (', piece.get_x(), ', ', piece.get_y(), ')')
