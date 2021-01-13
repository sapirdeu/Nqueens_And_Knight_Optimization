from ChessPiece import ChessPiece


class Knight(ChessPiece):
    # Ctor- initializes Knight's location and rules.
    def __init__(self, x, y):
        super(Knight, self).__init__(x, y)
        self.__name = "K"
        self.__rules = [lambda: {'x': self.get_x() - 2, 'y': self.get_y() + 1},
                        lambda: {'x': self.get_x() - 1, 'y': self.get_y() + 2},
                        lambda: {'x': self.get_x() + 1, 'y': self.get_y() + 2},
                        lambda: {'x': self.get_x() + 2, 'y': self.get_y() + 1},
                        lambda: {'x': self.get_x() + 2, 'y': self.get_y() - 1},
                        lambda: {'x': self.get_x() + 1, 'y': self.get_y() - 2},
                        lambda: {'x': self.get_x() - 1, 'y': self.get_y() - 2},
                        lambda: {'x': self.get_x() - 2, 'y': self.get_y() - 1}]

    # Getters.
    def get_rules(self):
        return self.__rules

    def __str__(self):
        return self.__name
