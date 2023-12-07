import os
import sys
import tkinter as tk
import register
import board_render
import game_representation as game_rep
from time import sleep
import asyncio

font = 'Georgia 15'
show_password_setting = '*'


# ------------Functions
def window_in_center(work_window, w=100, h=100):
    ws = work_window.winfo_screenwidth()  # width of the screen
    hs = work_window.winfo_screenheight()  # height of the screen

    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    work_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return 'placed at: %dx%d+%d+%d' % (w, h, x, y)


# -------------Classes

class WindowManager:
    def __init__(self, master):
        self.register_window = None
        self.root_window = None
        self.login_window = master
        self.login_window.title("Вход в учётную запись")
        window_in_center(self.login_window, 600, 350)
        self.login_window.resizable(False, False)

        if not os.path.exists('users.json'):
            with open('users.json', 'w') as f:
                json.dump([], f)
                pass

        check = (self.login_window.register(register.password_ableness), "%P")
        #  ----------------------------------------------------

        label = tk.Label(text="Имя пользователя", font=font)
        label.pack()

        login_box = tk.Entry(font=font)
        login_box.place(x=155, y=45)

        label2 = tk.Label(text="Пароль", font=font)
        label2.place(x=250, y=90)

        password_box = tk.Entry(font=font, validate='key', validatecommand=check, show=show_password_setting)
        password_box.place(x=155, y=140)

        # show_pswrd_btn = tk.Button(text="Показать пароль", font='Georgia 9', command=show_password)
        # show_pswrd_btn.place(x=450, y=140)

        login_btn = tk.Button(text="Войти", font=font, command=lambda: (
        register.login(self.login_window, login_box, password_box), self.program_start(self.login_window)))
        login_btn.place(x=250, y=200)

        register_btn = tk.Button(text="Создать аккаунт", font=font, command=lambda: self.reg_window(self.login_window))
        register_btn.place(x=195, y=270)

        tk.mainloop()

    def reg_window(self, login_window):
        check = (login_window.register(register.password_ableness), "%P")
        self.register_window = tk.Toplevel(self.login_window)
        # this forces all focus on the top level until Toplevel is closed
        self.register_window.grab_set()
        self.register_window.title("Регистрация")
        self.register_window.resizable(False, False)
        window_in_center(self.register_window, 600, 280)

        label = tk.Label(self.register_window, text="Имя пользователя", font=font)
        label.pack()

        reg_login_box = tk.Entry(self.register_window, font=font)
        reg_login_box.place(x=155, y=45)

        label = tk.Label(self.register_window, text="Придумайте пароль", font=font)
        label.place(x=190, y=90)

        reg_password_box = tk.Entry(self.register_window, font=font, validate='key', validatecommand=check,
                                    show=show_password_setting)
        reg_password_box.place(x=155, y=140)

        # global reg_show_pswrd_btn
        # reg_show_pswrd_btn = tk.Button(window, text="Показать пароль", font='Georgia 9', command=show_password)
        # reg_show_pswrd_btn.place(x=450, y=140)

        login_btn = tk.Button(self.register_window, text="Регистрация", font=font,
                              command=lambda: register.register(self.register_window, reg_login_box, reg_password_box))
        login_btn.place(x=215, y=200)

    def program_start(self, login_window):
        if register.pass_flag._value:
            login_window.destroy()
            self.root_window = tk.Tk()
            self.root_window.title("Chess endgame")
            self.root_window.configure(bg='#dfd3b1')
            window_in_center(self.root_window, 1000, 1000)

            board_canvas = tk.Canvas(self.root_window, background='#dfd3b1', height=801, width=801,
                                     highlightthickness=0)
            board_canvas.place(x=100, y=100)

            board_object = game_rep.GameBoard()
            board_object.random_content()
            board_render.draw_board(board_canvas, board_object, 800, 800)

            board_canvas.bind("<Button-1>", lambda event: board_render.detect_square(event, board_canvas, board_object, board_object.figure_dict['black_king']))


# ------------Programm initializaion

start_window = tk.Tk()
app = WindowManager(start_window)

# ------------Board-drawing
