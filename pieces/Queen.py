from ChessPiece import ChessPiece


class Queen(ChessPiece):
    # Ctor- initializes Queen's location and rules.
    def __init__(self, x, y):
        super(Queen, self).__init__(x, y)
        self.__name = "Q"
        self.__rules = [lambda i: {'x': self.get_x() + i, 'y': self.get_y()},
                        lambda i: {'x': self.get_x() - i, 'y': self.get_y()},
                        lambda i: {'x': self.get_x(), 'y': self.get_y() + i},
                        lambda i: {'x': self.get_x(), 'y': self.get_y() - i},
                        lambda i: {'x': self.get_x() + i, 'y': self.get_y() + i},
                        lambda i: {'x': self.get_x() + i, 'y': self.get_y() - i},
                        lambda i: {'x': self.get_x() - i, 'y': self.get_y() + i},
                        lambda i: {'x': self.get_x() - i, 'y': self.get_y() - i}]

    # Getters.
    def get_rules(self):
        return self.__rules

    def __str__(self):
        return self.__name
