import argparse
import socket
import sys
import select
import logs.configs.server_cnf
from logging import getLogger
from decos import log

from Lesson_8.common.variables import ACTION, PRESENCE, TIME, USER, ACC_NAME, ERROR, \
    DEF_PORT, DEF_IP_ADR, MAX_CON, MESSAGE, MESS_TEXT, SENDER, RESP_200, RESP_400, DEST, EXIT
from Lesson_8.common.utils import get_message, send_message

SERVER_LOGGER = getLogger('server')


@log
def proc_client_message(message, messages_list, client, clients, names):
    SERVER_LOGGER.debug('Разбор сообщения от клиента')
    if ACTION in message and message[ACTION] == PRESENCE and \
            TIME in message and USER in message:
        if message[USER][ACC_NAME] not in names.keys():
            names[message[USER][ACC_NAME]] = client
            send_message(client, RESP_200)
        else:
            response = RESP_400
            response[ERROR] = 'Имя пользователя уже занято.'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    elif ACTION in message and message[ACTION] == MESSAGE and \
            DEST in message and TIME in message \
            and SENDER in message and MESS_TEXT in message:
        messages_list.append(message)
        return
    elif ACTION in message and message[ACTION] == EXIT and ACC_NAME in message:
        clients.remove(names[message[ACC_NAME]])
        names[message[ACC_NAME]].close()
        del names[message[ACC_NAME]]
        return
    else:
        response = RESP_400
        response[ERROR] = 'Запрос некорректен.'
        send_message(client, response)
        return


@log
def proc_message(message, names, listen_socks):
    if message[DEST] in names and names[message[DEST]] in listen_socks:
        send_message(names[message[DEST]], message)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DEST]} '
                           f'от пользователя {message[SENDER]}.')
    elif message[DEST] in names and names[message[DEST]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.error(
            f'Пользователь {message[DEST]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


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

    names = dict()

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
                                        messages, client_with_message, clients, names)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                       f'отключился от сервера.')
                    clients.remove(client_with_message)

        for m in messages:
            try:
                proc_message(m, names, send_data_lst)
            except Exception:
                SERVER_LOGGER.info(f'Связь с клиентом с именем {m[DEST]} была потеряна')
                clients.remove(names[m[DEST]])
                del names[m[DEST]]
        messages.clear()


if __name__ == '__main__':
    SERVER_LOGGER.info('Сервер запущен')
    print('-- Сервер запущен --')
    main()
