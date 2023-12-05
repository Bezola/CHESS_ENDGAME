class Figure():
    def __init__(self, color, place):
        self.color = color
        self.place = place

class King(Figure):
    def __init__(self, color, place):
        super().__init__(color, place)
        self.f_type = 'King'
        if self.color == 'Black':
            self.photopath = 'C:\\Users\\Roman-laptop\\PycharmProjects\\CHESS_ENDGAME\\venv\\imgs\\black-king.png'
        elif self.color == 'White':
            self.photopath = 'C:\\Users\\Roman-laptop\\PycharmProjects\\CHESS_ENDGAME\\venv\\imgs\\white-king.png'

class Rook(Figure):
    def __init__(self, *args, **kw):
        self.f_type = 'Rook'

class Queen(Figure):
    def __init__(self, *args, **kw):
        self.f_type = 'Queen'
        if self.color == 'Black':
            self.photopath = 'imgs/black-queen.png'
        elif self.color == 'White':
            self.photopath = 'imgs/white-queen.png'