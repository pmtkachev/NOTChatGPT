"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

words = ['разработка', 'администрирование', 'protocol', 'standard']


def to_bytes(lst):
    words_b = []
    for i in lst:
        words_b.append(i.encode())
        print(f'{i.encode()} - {type(i.encode())}')
    return words_b


def to_string(lst):
    for i in lst:
        print(f'{i.decode()} - {type(i.decode())}')


to_string(to_bytes(words))
