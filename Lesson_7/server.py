import argparse
import json
import socket
import sys
import time

import select

import logs.configs.server_cnf
from logging import getLogger
from decos import log

from Lesson_7.common.variables import ACTION, PRESENCE, TIME, USER, ACC_NAME, RESPONSE, ERROR, \
    DEF_PORT, DEF_IP_ADR, MAX_CON, MESSAGE, MESS_TEXT, SENDER
from Lesson_7.common.utils import get_message, send_message

SERVER_LOGGER = getLogger('server')


@log
def proc_client_message(message, messages_list, client):
    SERVER_LOGGER.debug('Разбор сообщения от клиента')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACC_NAME] == 'Anonim':
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESS_TEXT in message:
        messages_list.append((message[ACC_NAME], message[MESS_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEF_PORT, type=int, nargs='?')
    parser.add_argument('-a', default=DEF_IP_ADR, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_addr = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_addr, listen_port


def main():
    listen_addr, listen_port = arg_parser()

    SERVER_LOGGER.info(
        f'Запущен сервер, порт для подключений: {listen_port}, '
        f'адрес с которого принимаются подключения: {listen_addr}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_addr, listen_port))
    transport.settimeout(1)

    clients = []
    messages = []

    transport.listen(MAX_CON)
    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соедение с клиентом: {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    proc_client_message(get_message(client_with_message),
                                        messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                       f'отключился от сервера.')
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESS_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)


if __name__ == '__main__':
    SERVER_LOGGER.info('Сервер запущен')
    print('-- Сервер запущен --')
    main()
