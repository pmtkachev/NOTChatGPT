"""Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор». Проверить кодировку
файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое."""
import chardet

with open('test_file.txt', 'rb') as file:
    print(f"Кодировка по умолчанию: {chardet.detect(file.read())['encoding']}")

with open('test_file.txt', encoding='UTF-8', errors='replace') as file:
    print(file.read())
