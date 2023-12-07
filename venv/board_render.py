import tkinter as tk
from PIL import Image, ImageTk
import game_representation as game_rep


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
                for figure_name in ['black_king', 'white_king', 'rook', 'queen']:
                    if board_object.figure_dict[figure_name].return_photo_by_int(board_object.board_matrix[i][j])[0]:
                        board_canvas.create_image(place_x + 10, place_y + 10, anchor='nw',
                                                  image=board_object.figure_dict[figure_name].return_photo_by_int(board_object.board_matrix[i][j])[1])
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


def detect_square(event, board_canvas, board_object, figure):
    x = event.x // 100
    y = event.y // 100
    click_coord = [x, y]

    draw_move(board_canvas, board_object, figure, click_coord)

