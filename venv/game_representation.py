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
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\king_black.png')).resize((80, 80)))
        elif self.color == 'White':
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\king_white.png')).resize((80, 80)))


class Rook(Figure):
    def __init__(self, color, place):
        super().__init__(color, place)
        self.f_type = 'Rook'
        if self.color == 'Black':
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\rook_black.png')).resize((80, 80)))
        elif self.color == 'White':
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\rook_white.png')).resize((80, 80)))


class Queen(Figure):
    def __init__(self, *args, **kw):
        super().__init__(color, place)
        self.f_type = 'Queen'
        if self.color == 'Black':
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\queen_black.png')).resize((80, 80)))
        elif self.color == 'White':
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\queen_white.png')).resize((80, 80)))
