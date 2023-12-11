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
        self.temp_matrix = None
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

    def generate_moves(self, figure, func_recall=True, move_side=None, board_matrix=None):  # Просчёт правомерных ходов
        if move_side is None:
            move_side = self.move_side
        if board_matrix is None:
            board_matrix = self.board_matrix
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
                            if board_matrix[figure.place[0] + check_x][
                                figure.place[1] + check_y] * move_side < 0:  # Фигуры противника
                                lawfulcaptures_list.append([figure.place[0] + check_x, figure.place[1] + check_y])
                                if board_matrix[figure.place[0] + check_x][figure.place[1] + check_y] * move_side == -4:
                                    check_x, check_y = check_x + x, check_y + y
                                else:
                                    break
                            elif board_matrix[figure.place[0] + check_x][
                                figure.place[1] + check_y] * move_side > 0:  # Свои фигуры
                                break
                            else:
                                lawfulmoves_list.append([figure.place[0] + check_x, figure.place[1] + check_y])
                                check_x, check_y = check_x + x, check_y + y

        if type(figure) is King and func_recall:
            for figure_name in ['black_king', 'white_king', 'rook',
                                'queen']:  # Удаление ходов подставляющих короля под бой
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
        elif func_recall:
            for king_name in ['black_king', 'white_king']:
                if king_name in self.figure_dict and self.figure_dict[king_name].color == figure.color:
                    friend_king_obj = self.figure_dict[king_name]
                    if self.isKingInCheck(friend_king_obj,
                                          self.move_side * -1) and func_recall:  # Если король под шахом
                        lawfulmoves_list, lawfulcaptures_list = self.moves_availability(figure)
        return [lawfulmoves_list, lawfulcaptures_list]

    def isKingInCheck(self, king, move_side=None):
        if move_side is None:
            move_side = self.move_side
        for figure_name in ['rook', 'queen']:
            if figure_name in self.figure_dict and king.place in \
                    self.generate_moves(self.figure_dict[figure_name], False, move_side=move_side)[1]:
                if self.figure_dict[figure_name].f_type * move_side > 0:
                    king.IsChecked = True
                    return king.IsChecked
            else:
                king.IsChecked = False
        return king.IsChecked

    def moves_availability(self, friend_piece):

        move_list, capture_list = [], []

        enemy_moves_matrix = np.zeros((8, 8))
        friend_moves_matrix = np.zeros((8, 8))
        for king_name in ['black_king', 'white_king']:
            if king_name in self.figure_dict and self.figure_dict[king_name].color == friend_piece.color:
                friend_king_obj = self.figure_dict[king_name]
                if self.isKingInCheck(friend_king_obj, self.move_side * -1):  # Если король под шахом
                    for enemy_piece_name in ['rook', 'queen']:
                        if (enemy_piece_name in self.figure_dict
                                and friend_king_obj.color != self.figure_dict[enemy_piece_name].color):
                            enemy_piece = self.figure_dict[enemy_piece_name]
                            friend_moves_matrix[enemy_piece.place[0]][enemy_piece.place[1]] = enemy_piece.f_type
                            friend_moves_matrix[friend_king_obj.place[0]][
                                friend_king_obj.place[1]] = friend_king_obj.f_type
                            for enemy_move in \
                                    self.generate_moves(enemy_piece, False, self.move_side * -1, enemy_moves_matrix)[0]:
                                enemy_moves_matrix[enemy_move[0]][enemy_move[1]] = 1

                            for friend_capture in \
                                    self.generate_moves(friend_piece, False, self.move_side, friend_moves_matrix)[
                                        1]:  # Делаем проверку на съедобность вражеской фигуры
                                if enemy_piece.place == friend_capture:
                                    capture_list.append(enemy_piece.place)

                            for friend_move in \
                                    self.generate_moves(friend_piece, False, self.move_side, friend_moves_matrix)[
                                        0]:  # Делаем проверку на перекрытие фигурой
                                friend_moves_matrix[friend_move[0]][friend_move[1]] = 1

                            for x in range(min(friend_king_obj.place[0], enemy_piece.place[0]),
                                           max(friend_king_obj.place[0], enemy_piece.place[0]) + 1):
                                for y in range(min(friend_king_obj.place[1], enemy_piece.place[1]),
                                               max(friend_king_obj.place[1], enemy_piece.place[1]) + 1):
                                    if enemy_moves_matrix[x][y] == 1 and friend_moves_matrix[x][y] == 1:
                                        if (friend_king_obj.place[0] != enemy_piece.place[0]
                                                and friend_king_obj.place[1] != enemy_piece.place[1]):
                                            if x != enemy_piece.place[0] and y != enemy_piece.place[1]:
                                                move_list.append([x, y])
                                        else:
                                            move_list.append([x, y])
        return move_list, capture_list

    def isGameEnded(self):
        avaliable_moves_list = []
        for king_obj in [self.figure_dict['black_king'], self.figure_dict['white_king']]:
            if king_obj.f_type * self.move_side == 4:
                check_list = [king_obj]
                for piece_name in ['rook', 'queen']:
                    if piece_name in self.figure_dict and king_obj.color == self.figure_dict[piece_name].color:
                        check_list.append(self.figure_dict[piece_name])
                    for figure in check_list:
                        for move_list in self.generate_moves(figure):
                            avaliable_moves_list += move_list

                    if self.isKingInCheck(king_obj, self.move_side * -1) and len(avaliable_moves_list) == 0:
                        won_color = ['White', 'Black']
                        won_color.remove(king_obj.color)
                        return [True, won_color[0] + ' won']
                    elif len(avaliable_moves_list) == 0 or self.board_matrix.sum() == 0:
                        return [True, 'Draw']
        return [False, 'Waiting to move']