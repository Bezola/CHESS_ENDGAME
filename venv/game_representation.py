from PIL import Image, ImageTk

class Figure():
    def __init__(self, color, place):
        self.color = color
        self.place = place


class King(Figure):
    def __init__(self, color, place):
        super().__init__(color, place)
        self.f_type = 'King'
        if self.color == 'Black':
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\black-king.png')).resize((80, 80)))
        elif self.color == 'White':
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\white-king.png')).resize((80, 80)))


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
