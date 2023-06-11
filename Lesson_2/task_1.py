"""Задание на закрепление знаний по модулю CSV.
Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV."""

import csv
import re

files_list = [f'info_{i}.txt' for i in range(1, 4)]


def get_data(files):
    dev_reg = re.compile(r'Изготовитель системы:\s*\S*')
    os_reg = re.compile(r'Название ОС:\s*\S*\s*\S*\s*\S*')
    code_reg = re.compile(r'Код продукта:\s*\S*')
    type_reg = re.compile(r'Тип системы:\s*\S*')

    main_data = [['Изготовитель системы', 'Название ОС',
                  'Код продукта', 'Тип системы']]
    dev_list = []
    os_list = []
    code_list = []
    type_list = []

    for file in files:
        with open(file) as f:
            read_file = f.read()
            dev_list.append(dev_reg.findall(read_file)[0].split()[2])
            os_list.append(' '.join((os_reg.findall(read_file)[0]).split()[3:]))
            code_list.append(code_reg.findall(read_file)[0].split()[2])
            type_list.append(type_reg.findall(read_file)[0].split()[2])

    for i in range(3):
        main_data.append([dev_list[i], os_list[i], code_list[i], type_list[i]])

    return main_data


def write_to_csv(data):
    with open('data.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data)


write_to_csv(get_data(files_list))
