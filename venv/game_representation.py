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
        self.figure_dict = {
            'black_king': None,
            'white_king': None,
            'rook': None,
            'queen': None
        }
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

        for figure_name in ['black_king', 'white_king', 'rook', 'queen']:
            while True:
                temp = [random.randint(0, 7), random.randint(0, 7)]
                if temp not in cords_list:
                    cords_list.append(temp)
                    if figure_name == 'white_king':
                        self.figure_dict[figure_name] = King('White', temp)
                    if figure_name == 'rook':
                        self.figure_dict[figure_name] = Rook(['White', 'Black'][start_figures_id], temp)
                    if figure_name == 'queen':
                        if start_figures_id == 0:
                            start_figures_id = 1
                        else:
                            start_figures_id = 0
                        self.figure_dict[figure_name] = Queen(['White', 'Black'][start_figures_id], temp)
                    break
            temp = self.figure_dict[figure_name].place
            self.board_matrix[temp[0]][temp[1]] = self.figure_dict[figure_name].f_type
        print(self.board_matrix.transpose())


def generate_moves(board_obj, figure):
    lawfulmoves_list = []
    lawfulcaptures_list = []

    if type(figure) is not King:  # Ходы для ладьи и Королевы
        for x in [-1, 1]:
            check_x = x
            while (figure.place[0] + check_x) in range(8):  # Горизонталь
                if board_obj.board_matrix[figure.place[0] + check_x, figure.place[1]] * board_obj.move_side < 0:
                    lawfulcaptures_list.append([figure.place[0] + check_x, figure.place[1]])
                    break
                elif board_obj.board_matrix[figure.place[0] + check_x][figure.place[1]] * board_obj.move_side > 0:
                    break
                else:
                    lawfulmoves_list.append([figure.place[0] + check_x, figure.place[1]])
                    check_x += x
        for y in [-1, 1]:
            check_y = y
            while (figure.place[1] + check_y) in range(8):  # Вертикаль
                if board_obj.board_matrix[figure.place[0], figure.place[1] + check_y] * board_obj.move_side < 0:
                    lawfulcaptures_list.append([figure.place[0], figure.place[1] + check_y])
                    break
                elif board_obj.board_matrix[figure.place[0]][figure.place[1] + check_y] * board_obj.move_side > 0:
                    break
                else:
                    lawfulmoves_list.append([figure.place[0], figure.place[1] + check_y])
                    check_y += y

        if type(figure) is Queen:  # Диагональ для королевы
            for x in [-1, 1]:
                for y in [-1, 1]:
                    check_x = x
                    check_y = y
                    while (figure.place[0] + check_x) in range(8) and (figure.place[1] + check_y) in range(8):
                        if board_obj.board_matrix[figure.place[0] + check_x][figure.place[1] + check_y] * board_obj.move_side < 0:
                            lawfulcaptures_list.append([figure.place[0] + check_x, figure.place[1] + check_y])
                            break
                        elif board_obj.board_matrix[figure.place[0] + check_x][figure.place[1] + check_y] * board_obj.move_side > 0:
                            break
                        else:
                            lawfulmoves_list.append([figure.place[0] + check_x, figure.place[1] + check_y])
                            check_x, check_y = check_x + x, check_y + y
    else:
        for x in range(8):
            if figure.place[0] != x and figure.place[0] - 2 < x < figure.place[0] + 2:  # Горизонталь
                if board_obj.board_matrix[x, figure.place[1]] * board_obj.move_side < 0:
                    lawfulcaptures_list.append([x, figure.place[1]])
                    break
                else:
                    lawfulmoves_list.append([x, figure.place[1]])
        for y in range(8):
            if figure.place[1] != y and figure.place[1] - 2 < y < figure.place[1] + 2:  # Вертикаль
                if board_obj.board_matrix[figure.place[0], y] * board_obj.move_side < 0:
                    lawfulcaptures_list.append([figure.place[0], y])
                    break
                else:
                    lawfulmoves_list.append([figure.place[0], y])

        for x in [-1, 1]:  # Диагональ
            for y in [-1, 1]:
                if board_obj.board_matrix[figure.place[0] + x][figure.place[1] + y] * board_obj.move_side < 0:
                    lawfulcaptures_list.append([figure.place[0] + x, figure.place[1] + y])
                elif board_obj.board_matrix[figure.place[0] + x][figure.place[1] + y] * board_obj.move_side > 0:
                    pass
                else:
                    lawfulmoves_list.append([figure.place[0] + x, figure.place[1] + y])

    return [lawfulmoves_list, lawfulcaptures_list]
