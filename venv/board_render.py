import tkinter as tk
from PIL import Image, ImageTk
import game_representation as game_rep


def draw_board(board_canvas, height=800, width=800):
    quad_h, quad_w, place_x, place_y = height / 8, width / 8, 0, 0
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                color = '#d4c387'  # Тёмный
            else:
                color = '#f0ead4'  # Светлый
            board_canvas.create_rectangle(place_x, place_y, quad_w, quad_h, fill=color, outline="#004D40")
            place_y += 100
            quad_h += 100
        place_y, quad_h = 0, 100
        place_x += 100
        quad_w += 100


def detect_square(event, board_canvas, white_king):
    x = event.x // 100
    y = event.y // 100
    print(x * 100, y * 100)
    board_canvas.delete("all"), draw_board(board_canvas)
    event.widget.create_image(x * 100 + 10, y * 100 + 10, anchor='nw', image=white_king.photo)
    # event.widget.create_text(specially_wrong_parameter=None)
