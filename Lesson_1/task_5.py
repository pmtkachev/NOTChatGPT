"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""
import chardet
import subprocess

PING_YANDEX = subprocess.Popen(['ping', 'yandex.ru'], stdout=subprocess.PIPE)
PING_YOUTUBE = subprocess.Popen(['ping', 'youtube.com'], stdout=subprocess.PIPE)


def to_kir(site):
    for line in site.stdout:
        res = chardet.detect(line)
        print(line.decode(encoding=res['encoding']))


to_kir(PING_YOUTUBE)
to_kir(PING_YANDEX)
