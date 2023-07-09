import argparse
import json
import socket
import sys
import threading
import time
import logs.configs.client_cnf
from decos import log
from logging import getLogger
from common.variables import ACTION, PRESENCE, TIME, USER, ACC_NAME, \
    RESPONSE, ERROR, DEF_PORT, DEF_IP_ADR, MESSAGE, SENDER, MESS_TEXT, \
    EXIT, DEST
from common.utils import send_message, get_message
from mclases import ClientMake

LOGGER_CLIENT = getLogger('client')


# Отправка сообщения на сервер
class ClientSend(threading.Thread, metaclass=ClientMake):
    def __init__(self, acc_name, sock):
        self.acc_name = acc_name
        self.sock = sock
        self.cmnds = {'e': 'выход из программы',
                      'h': 'вывести подсказки по командам',
                      'm': 'отправить сообщение'}
        super().__init__()

    def help_chat(self):
        print('Команды чата: ')
        for k, v in self.cmnds.items():
            print(f'{k} - {v}.')

    def exit_message(self):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACC_NAME: self.acc_name
        }

    def create_message(self):
        to_user = input('Кому отправить?: ')
        message = input('Сообщение: ')
        message_dict = {
            ACTION: MESSAGE,
            TIME: time.time(),
            SENDER: self.acc_name,
            MESS_TEXT: message,
            DEST: to_user,

        }
        LOGGER_CLIENT.debug(f'Сформирован словарь сообщения: {message_dict}')
        try:
            send_message(self.sock, message_dict)
            LOGGER_CLIENT.info(f'Отправлено сообщение для пользователя {to_user}')
        except:
            LOGGER_CLIENT.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def run(self):
        self.help_chat()

        while True:
            cmnd = input('Команда: ')
            if cmnd == 'm':
                self.create_message()
            elif cmnd == 'h':
                self.help_chat()
            elif cmnd == 'e':
                send_message(self.sock, self.exit_message())
                print('Завершение соединения.')
                LOGGER_CLIENT.info('Завершение работы по команде пользователя.')
                time.sleep(0.5)
                break
            else:
                print('Неизвестная команда, введи h для справки')


# Получение сообщений с сервера
class ClientRead(threading.Thread, metaclass=ClientMake):
    def __init__(self, acc_name, sock):
        self.acc_name = acc_name
        self.sock = sock
        super().__init__()

    def run(self):
        while True:
            try:
                message = get_message(self.sock)
                if ACTION in message and message[ACTION] == MESSAGE and \
                        SENDER in message and DEST in message \
                        and MESS_TEXT in message and message[DEST] == self.acc_name:
                    print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
                          f'\n{message[MESS_TEXT]}')
                    LOGGER_CLIENT.info(f'Получено сообщение от пользователя {message[SENDER]}:'
                                       f'\n{message[MESS_TEXT]}')
                else:
                    LOGGER_CLIENT.error(f'Получено некорректное сообщение с сервера: {message}')
            except (OSError, ConnectionError, ConnectionAbortedError,
                    ConnectionResetError, json.JSONDecodeError):
                LOGGER_CLIENT.critical(f'Потеряно соединение с сервером.')
                break


@log
def create_presence(account_name):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACC_NAME: account_name
        }
    }
    LOGGER_CLIENT.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


@log
def process_ans(message):
    LOGGER_CLIENT.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEF_IP_ADR, nargs='?')
    parser.add_argument('port', default=DEF_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_addr = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    if not 1023 < server_port < 65536:
        LOGGER_CLIENT.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    return server_addr, server_port, client_name


def main():
    print('-= NotChatGPT Мессенджер (клиент) =-')
    server_addr, server_port, client_name = arg_parser()

    if not client_name:
        client_name = input('Имя пользователя: ')

    LOGGER_CLIENT.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_addr}, '
        f'порт: {server_port}, имя пользователя: {client_name}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_addr, server_port))
        send_message(transport, create_presence(client_name))
        answer = process_ans(get_message(transport))
        LOGGER_CLIENT.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
    except json.JSONDecodeError:
        LOGGER_CLIENT.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ConnectionRefusedError:
        LOGGER_CLIENT.critical(
            f'Не удалось подключиться к серверу {server_addr} : {server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        receiver = ClientRead(client_name, transport)
        receiver.daemon = True
        receiver.start()

        ui = ClientSend(client_name, transport)
        ui.daemon = True
        ui.start()
        LOGGER_CLIENT.debug('Запущены процессы')

        while True:
            time.sleep(1)
            if receiver.is_alive() and ui.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
