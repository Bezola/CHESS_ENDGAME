import tkinter as tk
from PIL import Image, ImageTk
import game_representation as game_rep


def detect_figure(board_object, i, j):
    for figure_name in ['black_king', 'white_king', 'rook', 'queen']:
        if board_object.figure_dict[figure_name].return_photo_by_int(board_object.board_matrix[i][j])[0]:
            return board_object.figure_dict[figure_name]


# ----------------------
def draw_board(board_canvas, board_object, height=800, width=800):
    quad_h, quad_w, place_x, place_y = height / 8, width / 8, 0, 0
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                color = '#d4c387'  # Тёмный
            else:
                color = '#f0ead4'  # Светлый
            board_canvas.create_rectangle(place_x, place_y, quad_w, quad_h, fill=color, outline="#004D40")
            if board_object.board_matrix[i][j] != 0:
                board_canvas.create_image(place_x + 10, place_y + 10, anchor='nw',
                                          image=detect_figure(board_object, i, j).return_photo_by_int(
                                              board_object.board_matrix[i][j])[1])
            place_y += 100
            quad_h += 100
        place_y, quad_h = 0, 100
        place_x += 100
        quad_w += 100


def draw_move(board_canvas, board_object, figure, new_place):
    board_canvas.delete("all"), draw_board(board_canvas, board_object)
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


def detect_square(event, board_canvas, board_object):
    x = event.x // 100
    y = event.y // 100
    click_coord = [x, y]

    if click_coord != board_object.focus_square:
        if board_object.board_matrix[x][y] != 0:
            if board_object.move_side == 1:  # ВЫБОР ФИГУРЫ/ВЗЯТИЕ БЕЛЫХ
                if detect_figure(board_object, x, y).f_type > 0:
                    board_object.focus_square = click_coord
                    board_object.focus_figure = detect_figure(board_object, x, y)

                if board_object.focus_figure is not None:
                    if detect_figure(board_object, x, y).f_type < 0:
                        board_object.focus_square = click_coord
                        prev_coord = board_object.focus_figure.place

                        board_object.board_matrix[prev_coord[0]][prev_coord[1]] = 0
                        board_object.board_matrix[x][y] = board_object.focus_figure.f_type
                        draw_move(board_canvas, board_object, board_object.focus_figure, click_coord)
                        board_object.focus_figure = None
                        board_object.move_side *= -1

            else:  # ВЫБОР ФИГУРЫ/ВЗЯТИЕ ЧЕРНЫХ
                if detect_figure(board_object, x, y).f_type < 0:
                    board_object.focus_square = click_coord
                    board_object.focus_figure = detect_figure(board_object, x, y)

                if board_object.focus_figure is not None:
                    if detect_figure(board_object, x, y).f_type > 0:
                        board_object.focus_square = click_coord
                        prev_coord = board_object.focus_figure.place

                        board_object.board_matrix[prev_coord[0]][prev_coord[1]] = 0
                        board_object.board_matrix[x][y] = board_object.focus_figure.f_type
                        draw_move(board_canvas, board_object, board_object.focus_figure, click_coord)
                        board_object.focus_figure = None
                        board_object.move_side *= -1


        elif board_object.focus_figure is not None:
            prev_coord = board_object.focus_figure.place
            board_object.board_matrix[prev_coord[0]][prev_coord[1]] = 0
            board_object.board_matrix[x][y] = board_object.focus_figure.f_type
            draw_move(board_canvas, board_object, board_object.focus_figure, click_coord)
            board_object.move_side *= -1

            if detect_figure(board_object, x, y).f_type < 0:
                board_object.focus_square = click_coord
                prev_coord = board_object.focus_figure.place

                board_object.board_matrix[prev_coord[0]][prev_coord[1]] = 0
                board_object.board_matrix[x][y] = board_object.focus_figure.f_type
                board_object.focus_figure = None

            if detect_figure(board_object, x, y).f_type > 0:
                board_object.focus_square = click_coord
                prev_coord = board_object.focus_figure.place

                board_object.board_matrix[prev_coord[0]][prev_coord[1]] = 0
                board_object.board_matrix[x][y] = board_object.focus_figure.f_type
                board_object.focus_figure = None

        else:
            board_object.focus_figure, board_object.focus_square = None, [None, None]
