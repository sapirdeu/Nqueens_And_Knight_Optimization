class ChessPiece(object):

    # Ctor- initializes the location of the piece.
    def __init__(self, x, y):
        # Dictionary of the location.
        self.__position = {}

        # Sets values.
        self.__position['x'] = x
        self.__position['y'] = y

    # Getters.
    def get_x(self):
        return self.__position['x']

    def get_y(self):
        return self.__position['y']

    # Setters.
    def set_x(self, x):
        self.__position['x'] = x

    def set_y(self, y):
        self.__position['y'] = y