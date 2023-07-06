"""
Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
(использовать модуль tabulate). Таблица должна состоять из двух колонок
"""
import tabulate
from task_2 import host_range_ping


def host_range_ping_tab():
    print(tabulate.tabulate(host_range_ping('192.168.0.234', '192.168.0.240', False), headers='keys'))


if __name__ == '__main__':
    host_range_ping_tab()
