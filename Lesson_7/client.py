import argparse
import json
import socket
import sys
import time
import logs.configs.client_cnf
from decos import log
from logging import getLogger
from common.variables import ACTION, PRESENCE, TIME, USER, ACC_NAME, \
    RESPONSE, ERROR, DEF_PORT, DEF_IP_ADR, MESSAGE, SENDER, MESS_TEXT
from common.utils import send_message, get_message

LOGGER_CLIENT = getLogger('client')


@log
def message_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESS_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESS_TEXT]}')
        LOGGER_CLIENT.info(f'Получено сообщение от пользователя '
                           f'{message[SENDER]}:\n{message[MESS_TEXT]}')
    else:
        LOGGER_CLIENT.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def create_message(sock, account_name='Anonim'):
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        LOGGER_CLIENT.info('Завершение работы по команде пользователя.')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACC_NAME: account_name,
        MESS_TEXT: message
    }
    LOGGER_CLIENT.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
def create_presence(account_name='Anonim'):
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
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_addr = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        LOGGER_CLIENT.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        LOGGER_CLIENT.critical(f'Указан недопустимый режим работы {client_mode}, '
                               f'допустимые режимы: listen , send')
        sys.exit(1)

    return server_addr, server_port, client_mode


def main():
    server_addr, server_port, client_mode = arg_parser()

    LOGGER_CLIENT.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_addr}, '
        f'порт: {server_port}, режим работы: {client_mode}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_addr, server_port))
        send_message(transport, create_presence())
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
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER_CLIENT.error(f'Соединение с сервером {server_addr} было потеряно.')
                    sys.exit(1)

            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER_CLIENT.error(f'Соединение с сервером {server_addr} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
