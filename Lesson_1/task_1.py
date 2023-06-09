"""
Задание 1.

Каждое из слов «разработка», «сокет», «декоратор» представить
в буквенном формате и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать
в набор кодовых точек Unicode (НО НЕ В БАЙТЫ!!!)
и также проверить тип и содержимое переменных.

*Попытайтесь получить кодовые точки без онлайн-конвертера!
без хардкода!

Подсказки:
--- 'разработка' - буквенный формат
--- '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430' - набор кодовых точек
--- используйте списки и циклы, не дублируйте функции
"""


def to_unicode(lst):
    words_uni = []
    for u in lst:
        words_uni.append(u.encode('unicode_escape').decode())
    return words_uni


words = ['разработка', 'сокет', 'декоратор']


def func(lst):
    for string in lst:
        print(f'{string} - {type(string)}')


func(words)
func(to_unicode(words))
