"""
2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""
from ipaddress import ip_address
from task_1 import host_ping

start_ip, end_ip = '192.168.0.1', '192.168.0.5'


def host_range_ping(start, end, is_print):
    ip_start = ip_address(start)
    ip_end = ip_address(end)

    adrs = []

    while ip_start <= ip_end:
        adrs.append(ip_start)
        ip_start += 1

    print(adrs)

    return [adr for adr in host_ping(adrs, is_print)]


if __name__ == '__main__':
    host_range_ping(start_ip, end_ip, True)
