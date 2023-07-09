import argparse
import socket
import sys
import select
import logs.configs.server_cnf
from logging import getLogger
from decos import log
from mclases import ServerMake
from common.variables import ACTION, PRESENCE, TIME, USER, ACC_NAME, ERROR, \
    DEF_PORT, DEF_IP_ADR, MAX_CON, MESSAGE, MESS_TEXT, SENDER, RESP_200, RESP_400, DEST, EXIT
from common.utils import get_message, send_message
from descripts import Port

SERVER_LOGGER = getLogger('server')


class Server(metaclass=ServerMake):
    port = Port()

    def __init__(self, l_adr, l_port):
        self.l_adr = l_adr
        self.l_port = l_port
        self.clients = []
        self.msgs = []
        self.names = {}
        self.sock = None

    def proc_client_message(self, message, client):
        SERVER_LOGGER.debug('Разбор сообщения от клиента')
        if ACTION in message and message[ACTION] == PRESENCE and \
                TIME in message and USER in message:
            if message[USER][ACC_NAME] not in self.names.keys():
                self.names[message[USER][ACC_NAME]] = client
                send_message(client, RESP_200)
            else:
                response = RESP_400
                response[ERROR] = 'Имя пользователя уже занято.'
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return
        elif ACTION in message and message[ACTION] == MESSAGE and \
                DEST in message and TIME in message \
                and SENDER in message and MESS_TEXT in message:
            self.msgs.append(message)
            return
        elif ACTION in message and message[ACTION] == EXIT and ACC_NAME in message:
            self.clients.remove(self.names[message[ACC_NAME]])
            self.names[message[ACC_NAME]].close()
            del self.names[message[ACC_NAME]]
            return
        else:
            response = RESP_400
            response[ERROR] = 'Запрос некорректен.'
            send_message(client, response)
            return

    def proc_message(self, message, listen_socks):
        if message[DEST] in self.names and self.names[message[DEST]] in listen_socks:
            send_message(self.names[message[DEST]], message)
            SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DEST]} '
                               f'от пользователя {message[SENDER]}.')
        elif message[DEST] in self.names and self.names[message[DEST]] not in listen_socks:
            raise ConnectionError
        else:
            SERVER_LOGGER.error(
                f'Пользователь {message[DEST]} не зарегистрирован на сервере, '
                f'отправка сообщения невозможна.')

    def init_sock(self):
        SERVER_LOGGER.info(
            f'Запущен сервер, порт для подключений: {self.l_port}, '
            f'адрес с которого принимаются подключения: {self.l_adr}. '
            f'Если адрес не указан, принимаются соединения с любых адресов.')

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.l_adr, self.l_port))
        transport.settimeout(1)

        self.sock = transport
        self.sock.listen(MAX_CON)

    def run(self):
        self.init_sock()
        SERVER_LOGGER.info('Сервер запущен')
        print('-- Сервер запущен --')

        while True:
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                SERVER_LOGGER.info(f'Установлено соедение с клиентом: {client_address}')
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []

            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.proc_client_message(get_message(client_with_message), client_with_message)
                    except:
                        SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                           f'отключился от сервера.')
                        self.clients.remove(client_with_message)

            for m in self.msgs:
                try:
                    self.proc_message(m, send_data_lst)
                except Exception:
                    SERVER_LOGGER.info(f'Связь с клиентом с именем {m[DEST]} была потеряна')
                    self.clients.remove(self.names[m[DEST]])
                    del self.names[m[DEST]]
            self.msgs.clear()


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
    l_adr, l_port = arg_parser()
    server = Server(l_adr, l_port)
    server.run()


if __name__ == '__main__':
    main()
