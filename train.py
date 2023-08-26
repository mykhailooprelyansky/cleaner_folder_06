# import re
#


def sequence_buttons(string):
    str_lower = string.lower()

    NUMBER = (1, 11, 111, 1111, 11111, 2, 22, 222, 3, 33, 333, 4, 44,
              444, 5, 55, 555, 6, 66, 666, 7, 77, 777, 7777, 8, 88, 888,
              9, 99, 999, 9999, 0)

    LATTER = (".", ",", "?", "!", ":", 'a', 'b', 'c', 'd', 'e', 'f',
              'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
              'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', " ")

    TRANSLIT_DICT = {}

    for l, n in zip(LATTER, NUMBER):
        TRANSLIT_DICT[ord(l)] = n

    number_code = str_lower.translate(TRANSLIT_DICT)
    return number_code


print(sequence_buttons('Hi there!'))
