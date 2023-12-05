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


def detect_square(event):
    x = event.x // 100
    y = event.y // 100
    white_king = game_rep.King('White', [x, y])
    print(x * 100, y * 100)
    img = (Image.open(white_king.photopath)).resize((100, 100))
    rofl_image = ImageTk.PhotoImage(img)
    event.widget.create_rectangle(10, 10, 100, 100, fill='green', outline="#004D40")
    event.widget.create_image(x * 100, x * 100, anchor='nw' , image=rofl_image)
    event.widget.create_text(x * 100, y * 100, text=chr("U+2654"))
