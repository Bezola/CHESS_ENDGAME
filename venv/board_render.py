import tkinter as tk
from winsound import PlaySound, SND_FILENAME, SND_ASYNC
from PIL import Image, ImageTk
import game_representation as game_rep


def detect_figure(board_obj, i, j):
    for figure_name in ['black_king', 'white_king', 'rook', 'queen']:
        if (figure_name in board_obj.figure_dict and
                board_obj.figure_dict[figure_name].return_photo_by_int(board_obj.board_matrix[i][j])[0]):
            return board_obj.figure_dict[figure_name]
    return None


def draw_board(board_canvas, board_obj, height=800, width=800):
    quad_h, quad_w, place_x, place_y = height / 8, width / 8, 0, 0
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                color = '#d4c387'  # Тёмный
            else:
                color = '#f0ead4'  # Светлый
            board_canvas.create_rectangle(place_x, place_y, quad_w, quad_h, fill=color, outline="#004D40")
            if board_obj.board_matrix[i][j] != 0:
                board_canvas.create_image(place_x + 10, place_y + 10, anchor='nw',
                                          image=detect_figure(board_obj, i, j).return_photo_by_int(
                                              board_obj.board_matrix[i][j])[1])
            place_y += 100
            quad_h += 100
        place_y, quad_h = 0, 100
        place_x += 100
        quad_w += 100

    for i in ['black_king', 'white_king']:
        if i in board_obj.figure_dict and board_obj.isKingInCheck(board_obj.figure_dict[i], board_obj.move_side * -1):
            board_canvas.create_text(board_obj.figure_dict[i].place[0] * 100 + 75,
                                     board_obj.figure_dict[i].place[1] * 100 + 30, text="!", fill="#ff7a66",
                                     font='Arial 35')


def draw_move(board_canvas, board_obj, figure, new_place, label_show_side):
    board_canvas.delete("all"), draw_board(board_canvas, board_obj)
    if not figure.place[0] is None:
        if (figure.place[0] + figure.place[1]) % 2 == 0:
            color = '#D4D087'  # Тёмно-схоженный
        else:
            color = '#DDE9AE'  # Светло-схоженный
        board_canvas.create_rectangle(figure.place[0] * 100, figure.place[1] * 100, figure.place[0] * 100 + 100,
                                      figure.place[1] * 100 + 100, fill=color, outline="#004D40")
    figure.place = new_place
    if (figure.place[0] + figure.place[1]) % 2 == 0:
        color = '#D4D087'  # Тёмно-схоженный
    else:
        color = '#DDE9AE'  # Светло-схоженный
    board_canvas.create_rectangle(figure.place[0] * 100, figure.place[1] * 100, figure.place[0] * 100 + 100,
                                  figure.place[1] * 100 + 100, fill=color, outline="#004D40")
    board_canvas.create_image(figure.place[0] * 100 + 10, figure.place[1] * 100 + 10, anchor='nw', image=figure.photo)

    if board_obj.move_side == 1:
        label_show_side.config(text='Ход черных', bg='black', fg='white')
    else:
        label_show_side.config(text='Ход белых', bg='white', fg='black')

    for i in ['black_king', 'white_king']:
        if board_obj.figure_dict[i] is not None and board_obj.isKingInCheck(board_obj.figure_dict[i],
                                                                            board_obj.move_side):
            board_canvas.create_text(board_obj.figure_dict[i].place[0] * 100 + 75,
                                     board_obj.figure_dict[i].place[1] * 100 + 30, text="!", fill="#ff7a66",
                                     font='Arial 35')
            PlaySound('sounds\\check.wav', SND_FILENAME | SND_ASYNC)


def detect_square(event, board_canvas, board_obj, label_show_side, root_window, mode='game'):
    x = event.x // 100
    y = event.y // 100
    click_coord = [x, y]

    if mode == 'game':
        if click_coord != board_obj.focus_square:
            if board_obj.board_matrix[x][y] != 0:
                if board_obj.move_side == 1:  # ВЫБОР ФИГУРЫ/ВЗЯТИЕ БЕЛЫМИ
                    if detect_figure(board_obj, x, y).f_type > 0:
                        board_obj.focus_square = click_coord
                        board_obj.focus_figure = detect_figure(board_obj, x, y)

                        draw_lawful_moves(board_canvas, board_obj)

                    if board_obj.focus_figure is not None:
                        captures_list = board_obj.generate_moves(board_obj.focus_figure)[1]
                        temp_obj = detect_figure(board_obj, x, y)
                        if click_coord in captures_list and temp_obj.f_type < 0:
                            board_obj.figure_dict.pop((str(type(temp_obj)).lower()).split('.')[1][:-2])
                            board_obj.focus_square = click_coord
                            prev_coord = board_obj.focus_figure.place

                            board_obj.board_matrix[prev_coord[0]][prev_coord[1]] = 0
                            board_obj.board_matrix[x][y] = board_obj.focus_figure.f_type
                            draw_move(board_canvas, board_obj, board_obj.focus_figure, click_coord, label_show_side)
                            board_obj.focus_figure = None
                            board_obj.move_side *= -1
                            PlaySound('sounds\\capture.wav', SND_FILENAME | SND_ASYNC)

                else:  # ВЫБОР ФИГУРЫ/ВЗЯТИЕ ЧЕРНЫМИ
                    if detect_figure(board_obj, x, y).f_type < 0:
                        board_obj.focus_square = click_coord
                        board_obj.focus_figure = detect_figure(board_obj, x, y)

                        draw_lawful_moves(board_canvas, board_obj)

                    if board_obj.focus_figure is not None:
                        captures_list = board_obj.generate_moves(board_obj.focus_figure)[1]
                        temp_obj = detect_figure(board_obj, x, y)
                        if click_coord in captures_list and temp_obj.f_type > 0:
                            board_obj.figure_dict.pop((str(type(temp_obj)).lower()).split('.')[1][:-2])
                            board_obj.focus_square = click_coord
                            prev_coord = board_obj.focus_figure.place

                            board_obj.board_matrix[prev_coord[0]][prev_coord[1]] = 0
                            board_obj.board_matrix[x][y] = board_obj.focus_figure.f_type
                            draw_move(board_canvas, board_obj, board_obj.focus_figure, click_coord, label_show_side)
                            board_obj.focus_figure = None
                            board_obj.move_side *= -1

                            PlaySound('sounds\\move.wav', SND_FILENAME | SND_ASYNC)
                            PlaySound('sounds\\capture.wav', SND_FILENAME | SND_ASYNC)

            elif board_obj.focus_figure is not None and click_coord in \
                    board_obj.generate_moves(board_obj.focus_figure)[0]:
                prev_coord = board_obj.focus_figure.place
                board_obj.board_matrix[prev_coord[0]][prev_coord[1]] = 0
                board_obj.board_matrix[x][y] = board_obj.focus_figure.f_type
                draw_move(board_canvas, board_obj, board_obj.focus_figure, click_coord, label_show_side)
                board_obj.move_side *= -1

                if detect_figure(board_obj, x, y).f_type < 0:  # Черные ход на пустую клетку
                    board_obj.focus_square = click_coord
                    prev_coord = board_obj.focus_figure.place

                    board_obj.board_matrix[prev_coord[0]][prev_coord[1]] = 0
                    board_obj.board_matrix[x][y] = board_obj.focus_figure.f_type
                    board_obj.focus_figure = None

                    PlaySound('sounds\\move.wav', SND_FILENAME | SND_ASYNC)

                if detect_figure(board_obj, x, y).f_type > 0:  # Белые ход на пустую клетку
                    board_obj.focus_square = click_coord
                    prev_coord = board_obj.focus_figure.place

                    board_obj.board_matrix[prev_coord[0]][prev_coord[1]] = 0
                    board_obj.board_matrix[x][y] = board_obj.focus_figure.f_type
                    board_obj.focus_figure = None

                    PlaySound('sounds\\move.wav', SND_FILENAME | SND_ASYNC)

            else:
                board_canvas.delete('all'), draw_board(board_canvas, board_obj)
                board_obj.focus_figure, board_obj.focus_square = None, [None, None]
        if board_obj.isGameEnded()[0] and not board_obj.isGameStopped:
            l_conclusion = tk.Label(root_window, text=board_obj.isGameEnded()[1], font='Arial 35 bold', anchor='center', borderwidth=1, relief="solid", width=10)
            board_obj.isGameStopped = True
            canvas = tk.Canvas(root_window, background='#e8e6e3', height=181, width=401)
            rand_gen_btn = tk.Button(text="Случайная доска", font='Georgia 15', anchor='center', command=lambda:
            (board_obj.random_content(rand_gen_btn, create_btn, canvas, l_conclusion),
             draw_board(board_canvas, board_obj, 800, 800)))
            create_btn = tk.Button(text="Своя доска", font='Georgia 15', anchor='center')
            canvas.place(x=300, y=410)
            create_btn.place(x=430, y=430)
            rand_gen_btn.place(x=400, y=520)
            l_conclusion.place(x=340, y=330)
            label_show_side.config(text='Ход белых', bg='white', fg='black')
        for i in ['black_king', 'white_king']:
            if i in board_obj.figure_dict and board_obj.isKingInCheck(board_obj.figure_dict[i],
                                                                                board_obj.move_side):
                board_canvas.create_text(board_obj.figure_dict[i].place[0] * 100 + 75,
                                         board_obj.figure_dict[i].place[1] * 100 + 30, text="!", fill="#ff7a66",
                                         font='Arial 35')
    elif mode == 'create':
        print('kjdxfz')

def draw_lawful_moves(board_canvas, board_obj):
    board_canvas.delete('all'), draw_board(board_canvas, board_obj)
    for i in board_obj.generate_moves(board_obj.focus_figure)[0]:
        board_canvas.create_image(i[0] * 100 + 50, i[1] * 100 + 50, image=board_obj.move_indicator, anchor='center')
    for i in board_obj.generate_moves(board_obj.focus_figure)[1]:
        board_canvas.create_image(i[0] * 100 + 50, i[1] * 100 + 50, image=board_obj.capture_indicator, anchor='center')
