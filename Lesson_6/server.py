import json
import socket
import sys
import logs.configs.server_cnf
from logging import getLogger
from decos import log

from Lesson_4.common.variables import ACTION, PRESENCE, TIME, USER, ACC_NAME, RESPONSE, ERROR, \
    DEF_PORT, DEF_IP_ADR, MAX_CON
from Lesson_4.common.utils import get_message, send_message

SERVER_LOGGER = getLogger('server')


@log
def proc_client_message(message):
    SERVER_LOGGER.debug('Разбор сообщения от клиента')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACC_NAME] == 'Anonim':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEF_PORT
        if listen_port < 1024 or listen_port > 65535:
            SERVER_LOGGER.critical(f'Неподходящий порт для прослушивания {listen_port}')
            raise ValueError
    except IndexError:
        SERVER_LOGGER.error('После "-p" необходимо указать номер порта')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical('Порт должен быть в диапазоне от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_adr = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_adr = DEF_IP_ADR
    except IndexError:
        SERVER_LOGGER.error('После "-a" необходимо указать адрес для прослушивания')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_adr, listen_port))

    transport.listen(MAX_CON)

    while True:
        client, client_adr = transport.accept()
        SERVER_LOGGER.info(f'Установлено соединение с клиентом {client_adr}')
        try:
            message_from_client = get_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение от клиента: {message_from_client}')
            response = proc_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecoder):
            SERVER_LOGGER.error('Некорректное сообщение от клиента')
            client.close()


if __name__ == '__main__':
    SERVER_LOGGER.info('Сервер запущен')
    main()
