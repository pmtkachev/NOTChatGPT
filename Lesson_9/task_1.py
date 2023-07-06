"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping
будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел
должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять
их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес
сетевого узла должен создаваться с помощью функции ip_address().
"""
import subprocess
from ipaddress import ip_address

adr_list = ['192.168.0.1', '192.168.1.255', '127.0.0.1', 'ya.ru']


def host_ping(adr_ip, is_print):
    for adr in adr_ip:
        try:
            ip = ip_address(adr)
        except:
            ip = adr
        response = subprocess.run(['ping', '-n', '1', str(ip)])
        msg = 'узел доступен!' if response.returncode == 0 else 'узел не доступен!'
        if is_print:
            yield print(f'{ip} - {msg}')
        else:
            key = 'Reachable' if response.returncode == 0 else 'Unreachable'
            yield {key: ip}


if __name__ == '__main__':
    host_ping(adr_list, True)
