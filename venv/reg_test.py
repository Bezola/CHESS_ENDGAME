import string

pswrd_hardcode = string.ascii_lowercase + string.ascii_uppercase + '1234567890!@#$%^&*()_+'
vigenere_dict = dict(zip(pswrd_hardcode, range(len(pswrd_hardcode))))

def vigenere_code(arrived_message, mode='code', key='default'):
    arrived_list = list(arrived_message)
    sub_list, str_answer, count = [],'', 0
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
    print(str_answer)


vigenere_code('My_name_is_Nicholas_the_Second!')
vigenere_code('PCdnuxxbmx_8tvksqaMjMkidSynHqh^', 'decode')