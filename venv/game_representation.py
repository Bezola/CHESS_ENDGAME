from PIL import Image, ImageTk
import numpy as np
import random


class Figure:  # Класс-мать, от него объекты не создавать!
    def __init__(self, color, place):
        self.color = color
        self.place = place

    def return_photo_by_int(self, index):
        if index == self.f_type:
            return True, self.photo
        else:
            return False, None


class King(Figure):
    def __init__(self, color, place):
        super().__init__(color, place)
        self.f_type = 4
        self.IsChecked = False
        if self.color == 'Black':
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\king_black.png')).resize((80, 80)))
            self.f_type *= -1
        elif self.color == 'White':
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\king_white.png')).resize((80, 80)))


class Rook(Figure):
    def __init__(self, color, place):
        super().__init__(color, place)
        self.f_type = 5
        if self.color == 'Black':
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\rook_black.png')).resize((80, 80)))
            self.f_type *= -1
        elif self.color == 'White':
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\rook_white.png')).resize((80, 80)))


class Queen(Figure):
    def __init__(self, color, place):
        super().__init__(color, place)
        self.f_type = 6
        if self.color == 'Black':
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\queen_black.png')).resize((80, 80)))
            self.f_type *= -1
        elif self.color == 'White':
            self.photo = ImageTk.PhotoImage((Image.open('imgs\\queen_white.png')).resize((80, 80)))


class GameBoard:
    def __init__(self):
        self.move_indicator = ImageTk.PhotoImage((Image.open('imgs\\move-indicator.png')).resize((48, 36)))
        self.capture_indicator = ImageTk.PhotoImage((Image.open('imgs\\capture-indicator.png')).resize((100, 100)))
        self.figure_dict = {}
        self.board_matrix = np.zeros((8, 8))
        self.focus_square = [None, None]
        self.focus_figure = None
        self.move_side = 1  # white = 1, black = -1

    def random_content(self):
        self.figure_dict['black_king'] = King('Black', [random.randint(0, 7), random.randint(0, 7)])
        temp = self.figure_dict['black_king'].place
        self.board_matrix[temp[0]][temp[1]] = self.figure_dict['black_king'].f_type

        cords_list = [temp]
        start_figures_id = random.randint(0, 1)

        for figure_name in ['rook', 'queen', 'white_king']:
            while True:
                temp = [random.randint(0, 7), random.randint(0, 7)]
                if temp not in cords_list:
                    if (figure_name == 'white_king' and not self.isKingInCheck(King('White', temp)) and
                            (temp not in self.generate_moves(self.figure_dict['black_king'], False, -1)[0])):
                        self.figure_dict[figure_name] = King('White', temp)
                        cords_list.append(temp)
                        break
                    if figure_name == 'rook':
                        self.figure_dict[figure_name] = Rook(['White', 'Black'][start_figures_id], temp)
                        if self.isKingInCheck(self.figure_dict['black_king']):
                            self.figure_dict[figure_name] = self.figure_dict.pop(figure_name)
                        else:
                            cords_list.append(temp)
                            break
                    if figure_name == 'queen':
                        if self.figure_dict['rook'].f_type > 0:
                            start_figures_id = 1
                        else:
                            start_figures_id = 0
                        self.figure_dict[figure_name] = Queen(['White', 'Black'][start_figures_id], temp)
                        if self.isKingInCheck(self.figure_dict['black_king']):
                            self.figure_dict[figure_name] = self.figure_dict.pop(figure_name)
                        else:
                            cords_list.append(temp)
                            break
            temp = self.figure_dict[figure_name].place
            self.board_matrix[temp[0]][temp[1]] = self.figure_dict[figure_name].f_type
        print(self.board_matrix.transpose())

    def generate_moves(self, figure, func_recall=True, move_side=None):  # Просчёт правомерных ходов
        if move_side is None:
            move_side = self.move_side
        lawfulmoves_list = []
        lawfulcaptures_list = []

        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if [x, y] != [0, 0]:
                    check_x = x
                    check_y = y
                    while (figure.place[0] + check_x) in range(8) and (figure.place[1] + check_y) in range(8):
                        if ((type(figure) is King and (abs(check_x) > 1 or abs(check_y) > 1))
                                or (type(figure) is Rook and x != 0 and y != 0)):
                            break
                        else:
                            if self.board_matrix[figure.place[0] + check_x][figure.place[1] + check_y] * move_side < 0:  # Фигуры противника
                                lawfulcaptures_list.append([figure.place[0] + check_x, figure.place[1] + check_y])
                                if self.board_matrix[figure.place[0] + check_x][figure.place[1] + check_y] * move_side == -4:
                                    check_x, check_y = check_x + x, check_y + y
                                else:
                                    break
                            elif self.board_matrix[figure.place[0] + check_x][figure.place[1] + check_y] * move_side > 0:  # Свои фигуры
                                break
                            else:
                                lawfulmoves_list.append([figure.place[0] + check_x, figure.place[1] + check_y])
                                check_x, check_y = check_x + x, check_y + y

        if type(figure) is King and func_recall:
            for figure_name in ['black_king', 'white_king', 'rook', 'queen']:  # Удаление ходов подставляющих короля под бой
                if figure_name in self.figure_dict and (self.figure_dict[figure_name].f_type * move_side) < 0:
                    piece = self.figure_dict[figure_name]
                    if type(piece) is King:
                        for i in self.generate_moves(piece, False):
                            for lawless_move in i:
                                if lawless_move in lawfulmoves_list:
                                    lawfulmoves_list.remove(lawless_move)
                                if lawless_move in lawfulcaptures_list:
                                    lawfulcaptures_list.remove(lawless_move)
                    else:
                        for i in self.generate_moves(piece, move_side=move_side * -1):
                            for lawless_move in i:
                                if lawless_move in lawfulmoves_list:
                                    lawfulmoves_list.remove(lawless_move)
                                if lawless_move in lawfulcaptures_list:
                                    lawfulcaptures_list.remove(lawless_move)
        return [lawfulmoves_list, lawfulcaptures_list]

    def isKingInCheck(self, king, move_side=None):
        if move_side is None:
            move_side = self.move_side
        for figure_name in ['rook', 'queen']:
            if figure_name in self.figure_dict and king.place in self.generate_moves(self.figure_dict[figure_name], move_side=move_side)[1]:
                if self.figure_dict[figure_name].f_type * move_side > 0:
                    king.IsChecked = True
                    return king.IsChecked
            else:
                king.IsChecked = False
        return king.IsChecked

