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
        self.f_type = 7
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
        self.create_index = 0
        self.cords_list = []
        self.temp_matrix, self.isGameStopped = None, False
        self.move_indicator = ImageTk.PhotoImage((Image.open('imgs\\move-indicator.png')).resize((48, 36)))
        self.capture_indicator = ImageTk.PhotoImage((Image.open('imgs\\capture-indicator.png')).resize((100, 100)))
        self.figure_dict = {}
        self.board_matrix = np.zeros((8, 8))
        self.focus_square = [None, None]
        self.focus_figure = None
        self.move_side = 1  # white = 1, black = -1

    def random_content(self, rnd_btn=None, crt_btn=None, canvas=None, l_conclusion=None):
        if rnd_btn is not None:
            rnd_btn.destroy(), crt_btn.destroy(), canvas.destroy()
            self.isGameStopped, self.move_side = False, 1
        if l_conclusion is not None:
            l_conclusion.destroy()
        self.board_matrix = np.zeros((8, 8))

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

    def user_content(self, figure_name, start_figures_id, user_x, user_y):
        temp = [user_x, user_y]
        if temp not in self.cords_list:
            if figure_name == 'black_king':
                self.figure_dict['black_king'] = King('Black', [user_x, user_y])
                self.board_matrix[temp[0]][temp[1]] = self.figure_dict['black_king'].f_type
                self.cords_list.append(temp)
                return True

            if figure_name == 'white_king':
                if temp not in self.generate_moves(self.figure_dict['black_king'], False, -1)[0]:
                    self.figure_dict[figure_name] = King('White', temp)
                    self.cords_list.append(temp)
                else:
                    return False
            if figure_name == 'rook':
                self.figure_dict[figure_name] = Rook(['White', 'Black'][start_figures_id], temp)
                if self.isKingInCheck(self.figure_dict['black_king']):
                    self.figure_dict[figure_name] = self.figure_dict.pop(figure_name)
                    return False
                else:
                    self.cords_list.append(temp)
            if figure_name == 'queen':
                if self.figure_dict['rook'].f_type > 0:
                    start_figures_id = 1
                else:
                    start_figures_id = 0
                self.figure_dict[figure_name] = Queen(['White', 'Black'][start_figures_id], temp)
                if self.isKingInCheck(self.figure_dict['black_king']):
                    self.figure_dict[figure_name] = self.figure_dict.pop(figure_name)
                    return False
                else:
                    self.cords_list.append(temp)
            temp = self.figure_dict[figure_name].place
            self.board_matrix[temp[0]][temp[1]] = self.figure_dict[figure_name].f_type
            return True
        return False

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
                        temp_matrix = board_matrix.copy()
                        temp_matrix[piece.place[0]][piece.place[1]], temp_matrix[figure.place[0]][figure.place[1]] = 0, 0
                        for i in self.generate_moves(piece, False, move_side * -1, temp_matrix):
                            for lawless_move in i:
                                if lawless_move in lawfulmoves_list:
                                    lawfulmoves_list.remove(lawless_move)
                                if lawless_move in lawfulcaptures_list:
                                    lawfulcaptures_list.remove(lawless_move)
        elif func_recall and type(figure) is not King:
            lawfulmoves_list, lawfulcaptures_list = self.moves_availability(figure, lawfulmoves_list,
                                                                            lawfulcaptures_list)
        return [lawfulmoves_list, lawfulcaptures_list]

    def isKingInCheck(self, king, move_side=None, game_matrix=None, figure_dict=None):
        if move_side is None:
            move_side = self.move_side
        if game_matrix is None:
            game_matrix = self.board_matrix
        if figure_dict is None:
            figure_dict = self.figure_dict
        for figure_name in ['rook', 'queen']:
            if figure_name in figure_dict and king.place in \
                    self.generate_moves(figure_dict[figure_name], False, move_side=move_side,
                                        board_matrix=game_matrix)[1]:
                if self.figure_dict[figure_name].f_type * move_side > 0:
                    king.IsChecked = True
                    return king.IsChecked
            else:
                king.IsChecked = False
        return king.IsChecked

    def moves_availability(self, friend_piece, init_moves, init_captures):

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
                else:  # Привязка фигуры
                    for enemy_piece_name in ['rook', 'queen']:
                        if (enemy_piece_name in self.figure_dict
                                and friend_king_obj.color != self.figure_dict[enemy_piece_name].color):
                            enemy_piece = self.figure_dict[enemy_piece_name]
                            temp_matrix = self.board_matrix.copy()
                            temp_matrix[friend_piece.place[0]][friend_piece.place[1]] = 0

                            for friend_move in \
                                    self.generate_moves(friend_piece, False, self.move_side, friend_moves_matrix)[
                                        0]:  # Делаем проверку на перекрытие фигурой
                                friend_moves_matrix[friend_move[0]][friend_move[1]] = 1

                            for enemy_move in \
                                    self.generate_moves(enemy_piece, False, self.move_side * -1, enemy_moves_matrix)[0]:
                                enemy_moves_matrix[enemy_move[0]][enemy_move[1]] = 1
                            if friend_king_obj.place in \
                                    self.generate_moves(enemy_piece, False, self.move_side * -1, temp_matrix)[1]:
                                for x in range(min(friend_king_obj.place[0], enemy_piece.place[0]),
                                               max(friend_king_obj.place[0], enemy_piece.place[0]) + 1):
                                    for y in range(min(friend_king_obj.place[1], enemy_piece.place[1]),
                                                   max(friend_king_obj.place[1], enemy_piece.place[1]) + 1):
                                        if enemy_moves_matrix[x][y] == 1 and friend_moves_matrix[x][y] == 1:
                                            capture_list = init_captures
                                            if (friend_piece.place[0] != enemy_piece.place[0]
                                                    and friend_piece.place[1] != enemy_piece.place[1]):
                                                if x != enemy_piece.place[0] and y != enemy_piece.place[1]:
                                                    move_list.append([x, y])
                                            else:
                                                move_list.append([x, y])
                            else:
                                return init_moves, init_captures
                            try:
                                move_list.remove(friend_king_obj.place)
                            except ValueError:
                                pass
                            return move_list, capture_list

        return init_moves, init_captures

    '''def computer_search(self, depth, alpha=-float('inf'), beta=float('inf'), maximizing_player=False, local_move_side=None, game_matrix=None, figure_dict=None, final_move=False):
        figures_list = ['black_king', 'white_king', 'rook', 'queen']
        usable_piece_list = []
        if local_move_side is None:
            local_move_side = self.move_side
        if game_matrix is None:
            game_matrix = self.board_matrix.copy()
        if figure_dict is None:
            figure_dict = self.figure_dict.copy()
        # --------

        is_human_turn = not maximizing_player

        # children = board.get_all_possible_moves()
        children = []
        for figure_name in figures_list:
            if figure_name in figure_dict and (figure_dict[figure_name].f_type * local_move_side) > 0:
                usable_piece_list.append(figure_dict[figure_name])
                gen_list = self.generate_moves(figure_dict[figure_name], move_side=local_move_side,
                                               board_matrix=game_matrix)
                children.append(gen_list[0] + gen_list[1])
        if len(children) == 1:
            children.append([])
        # --------

        if depth == 0:
            return None, self.board_matrix.sum() * local_move_side
        elif len(children[0]) == 0 and len(children[1]) == 0:
            for king_obj in [figure_dict['black_king'], figure_dict['white_king']]:
                if king_obj.f_type * local_move_side > 0:
                    self.isKingInCheck(king_obj, move_side=local_move_side * -1)
                    if king_obj.IsChecked:
                        return None, -float('inf')
            return None, 0

        while True:
            try:
                best_piece = random.choice(usable_piece_list)
                temp = self.generate_moves(best_piece, move_side=local_move_side, board_matrix=game_matrix)
                best_move = random.choice(temp[0] + temp[1])
                break
            except IndexError:
                pass

        if maximizing_player:
            max_eval = -float('inf')
            for piece_index in range(len(children)):
                # if usable_piece_list[piece_index] in figure_dict:
                if children[piece_index]:
                    piece = usable_piece_list[piece_index]
                    for child in children[piece_index]:
                        temp_matrix = game_matrix.copy()
                        temp_f_dict = figure_dict.copy()
                        # board_copy.move(child)
                        temp_obj = detect_figure(figure_dict, game_matrix, child[0], child[1])
                        if temp_matrix[child[0]][child[1]] * local_move_side < 0 and temp_obj is not None:
                            temp_f_dict.pop((str(type(temp_obj)).lower()).split('.')[1][:-2])

                        temp_matrix[piece.place[0]][piece.place[1]] = 0  # make move
                        temp_matrix[child[0]][child[1]] = piece.f_type
                        # -------
                        current_eval = self.computer_search(depth - 1, alpha, beta, False, game_matrix=temp_matrix, local_move_side=local_move_side * -1, figure_dict=temp_f_dict)[1]
                        if current_eval > max_eval:
                            max_eval = current_eval
                            best_move, best_piece = child, piece
                        alpha = max(alpha, current_eval)
                        if beta <= alpha:
                            break
            if final_move:
                return best_move, best_piece
            return best_move, max_eval

        else:
            min_eval = float('inf')
            for piece_index in range(len(children)):
                # if usable_piece_list[piece_index] in figure_dict:
                if children[piece_index]:
                    piece = usable_piece_list[piece_index]
                    for child in children[piece_index]:
                        temp_matrix = game_matrix.copy()
                        temp_f_dict = figure_dict.copy()
                        # board_copy.move(child)
                        temp_obj = detect_figure(figure_dict, game_matrix, child[0], child[1])
                        if temp_matrix[child[0]][child[1]] * local_move_side < 0 and temp_obj is not None and type(temp_obj) is not King:
                            temp_f_dict.pop((str(type(temp_obj)).lower()).split('.')[1][:-2])

                        temp_matrix[piece.place[0]][piece.place[1]] = 0  # make move
                        temp_matrix[child[0]][child[1]] = piece.f_type
                        # -------
                        # current_eval = self.computer_search(board_copy, depth - 1, alpha, beta, True)[1]
                        current_eval = self.computer_search(depth - 1, alpha, beta, False, game_matrix=temp_matrix,
                                                            local_move_side=local_move_side * -1, figure_dict=temp_f_dict)[1]
                        if current_eval < min_eval:
                            min_eval = current_eval
                            best_move = child
                        beta = min(beta, current_eval)
                        if beta <= alpha:
                            break
            if final_move:
                return best_move, best_piece
            return best_move, min_eval'''

    def computer_search(self, depth=1, local_move_side=None, game_matrix=None, final_move=True, figure_dict=None,
                        alpha=-1000, beta=1000):
        figures_list = ['black_king', 'white_king', 'rook', 'queen']
        usable_piece_list = []
        moves = []

        if local_move_side is None:
            local_move_side = self.move_side
        if game_matrix is None and figure_dict is None:
            game_matrix, figure_dict = self.board_matrix.copy(), self.figure_dict.copy()

        if depth == 0:
            king_place_factor = 0
            for king_obj in [figure_dict['black_king'], figure_dict['white_king']]:
                if king_obj.f_type * local_move_side < 0:
                    king_place_factor -= (king_obj.place[0]) * 0.1
                    if self.isKingInCheck(king_obj, local_move_side, game_matrix):
                        king_place_factor += 0.3
                else:
                    king_place_factor += (abs(king_obj.place[0] - 3.5) + abs(king_obj.place[1] - 3.5)) * 0.01
                    '''if self.isKingInCheck(king_obj, local_move_side, game_matrix):
                        king_place_factor -= 0.3'''

            return (game_matrix.sum()) * local_move_side - king_place_factor

        best_evaluation = [None, None]
        while final_move:
            try:
                best_evaluation[1] = figure_dict[random.choice(figures_list)]
                if best_evaluation[1].color == 'Black':
                    temp = self.generate_moves(best_evaluation[1], move_side=local_move_side, board_matrix=game_matrix)
                    best_evaluation[0] = random.choice(temp[0] + temp[1])
                    break
            except IndexError:
                pass

        for figure_name in figures_list:
            if figure_name in figure_dict and (figure_dict[figure_name].f_type * local_move_side) > 0:
                usable_piece_list.append(figure_dict[figure_name])
                gen_list = self.generate_moves(figure_dict[figure_name], move_side=local_move_side,
                                               board_matrix=game_matrix)
                moves.append(gen_list[0] + gen_list[1])

        check_len = 0
        for i in range(len(moves)):
            check_len += len(moves[i])
        if check_len == 0:
            for king_obj in [figure_dict['black_king'], figure_dict['white_king']]:
                print(king_obj.f_type, self.isKingInCheck(king_obj, move_side=local_move_side,
                                                             game_matrix=game_matrix, figure_dict=figure_dict))
                if king_obj.f_type * local_move_side > 0 and self.isKingInCheck(king_obj, move_side=local_move_side,
                                                                        game_matrix=game_matrix, figure_dict=figure_dict):
                    print('засечка МАТ')
                    return -100000
            print('засечка ПАТ')
            return 0

        for piece_index in range(len(moves)):
            figure = usable_piece_list[piece_index]
            for move in moves[piece_index]:
                capture_flag = False
                temp_obj = detect_figure(figure_dict, game_matrix, move[0], move[1])
                if game_matrix[move[0]][move[1]] * local_move_side < 0 and temp_obj is not None and type(
                        temp_obj) is not King:
                    figure_dict.pop((str(type(temp_obj)).lower()).split('.')[1][:-2])
                    capture_flag = True

                game_matrix[figure.place[0]][figure.place[1]], prev_place = 0, figure.place  # make move
                temp = game_matrix[move[0]][move[1]]
                game_matrix[move[0]][move[1]], figure.place = figure.f_type, move

                print(move, 'depth =', depth, type(figure), figure.color)
                evaluation = -(
                    self.computer_search(depth - 1, local_move_side * -1, game_matrix, False,
                                         figure_dict, alpha=-beta, beta=-alpha))  # считаем глубже

                figure.place, game_matrix[figure.place[0]][
                    figure.place[1]] = prev_place, figure.f_type  # unmake move
                game_matrix[move[0]][move[1]] = temp
                if capture_flag:
                    figure_dict[(str(type(temp_obj)).lower()).split('.')[1][:-2]] = temp_obj

                if evaluation >= beta and not final_move:
                    # Не считать этот ход!
                    return beta
                if alpha < evaluation:
                    alpha, best_evaluation[0], best_evaluation[1] = evaluation, move, figure

        if final_move:
            print('ход выбран', alpha)
            return best_evaluation[0], best_evaluation[1]
        return alpha

    def isGameEnded(self):
        avaliable_moves_list = []
        for king_name in ['white_king', 'black_king']:
            if king_name in self.figure_dict:
                king_obj = self.figure_dict[king_name]
                if king_obj.f_type * self.move_side == 7:
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


def detect_figure(figure_dict, game_matrix, i, j):
    for figure_name in ['black_king', 'white_king', 'rook', 'queen']:
        if (figure_name in figure_dict and
                figure_dict[figure_name].return_photo_by_int(game_matrix[i][j])[0]):
            return figure_dict[figure_name]
    return None
