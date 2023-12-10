import json
import os
import re
import string
import tkinter as tk
from tkinter.messagebox import showwarning, showinfo

pswrd_hardcode = string.ascii_lowercase + string.ascii_uppercase + '1234567890!@#$%^&*()_+'
vigenere_dict = dict(zip(pswrd_hardcode, range(1, len(pswrd_hardcode) + 1)))


# ------------Classes

class objectWrapper:
    def __init__(self, initial_value):
        self._value = initial_value

    def __repr__(self):
        return repr(self._value)


pass_flag = objectWrapper(False)


# ------------Functions

def password_ableness(symbol):
    return re.fullmatch(r"[a-zA-Z\d!@#$%^&*()_+]*", symbol) is not None


def vigenere_code(arrived_message, mode='code', key='default'):
    arrived_list = list(arrived_message)
    sub_list, str_answer, count = [], '', 0
    for i in arrived_list:
        sub_list.append(key[count])
        count += 1
        if count >= len(key):
            count = 0

    for i in range(len(arrived_list)):
        if mode == 'code':
            new_char_num = vigenere_dict[arrived_list[i]] + vigenere_dict[sub_list[i]]
            if new_char_num > len(vigenere_dict):
                new_char_num -= len(vigenere_dict)
        if mode == 'decode':
            new_char_num = vigenere_dict[arrived_list[i]] - vigenere_dict[sub_list[i]]
            if new_char_num < 0:
                new_char_num += len(vigenere_dict)

        str_answer += list(vigenere_dict.keys())[list(vigenere_dict.values()).index(new_char_num)]
    return str_answer


def login(login_window, login_box, password_box):
    login_name = vigenere_code(login_box.get())
    password_name = vigenere_code(password_box.get())
    global pass_flag
    with open("users.json", "r") as read_file:
        try:
            users_data = list(json.load(read_file))
        except json.JSONDecodeError:
            users_data = None

    with open("users.json", "w") as file:  # Проверка на наличие пользователя в базе
        user_is_exists = False
        if users_data is not None:
            for user in users_data:
                if user['login'] == login_name and user['password'] == password_name:
                    user_is_exists = True
                    showinfo('Вход прошел успешно', 'Вход совершен')
                    pass_flag = objectWrapper(True)

        if not user_is_exists:
            if users_data is None:
                users_data = []
            showwarning('Ошибка', 'Неверное имя пользователя или пароль')
        json.dump(users_data, file)


def register(reg_window, reg_login_box, reg_password_box):
    login_name = vigenere_code(reg_login_box.get())
    password_name = vigenere_code(reg_password_box.get())
    if len(login_name) < 1:
        showwarning('Внимание', 'Имя не может быть короче 1 знака')
    else:
        if len(password_name) < 1:
            showwarning('Внимание', 'Пароль не может быть короче 1 знака')
        else:
            with open("users.json", "r") as read_file:
                try:
                    users_data = list(json.load(read_file))
                except json.JSONDecodeError:
                    users_data = None

            with open("users.json", "w") as f:  # Проверка на наличие пользователя в базе
                user_is_exists = False
                if users_data is not None:
                    for user in users_data:
                        if user['login'] == login_name:
                            user_is_exists = True
                            showwarning('Ошибка', 'Такое имя пользователя уже используется.')
                            json.dump(users_data, f)

                else:
                    users_data = []
                if not user_is_exists:
                    users_data.append({'login': login_name, "password": password_name})
                    # print('пользователь', login_name, 'зарегестрирован')
                    showinfo('Запись создана', 'Вы успешно зарегестрированы!')
                    json.dump(users_data, f)
                    reg_window.destroy()
