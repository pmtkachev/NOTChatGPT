import json
import socket
import sys
import time
from Lesson_4.common.variables import ACTION, PRESENCE, TIME, USER, ACC_NAME, \
    RESPONSE, ERROR, DEF_PORT, DEF_IP_ADR
from Lesson_4.common.utils import send_message, get_message


def create_presence(account_name='Anonim'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACC_NAME: account_name
        }
    }
    return out


def process_ans(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    try:
        server_adr = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 6535:
            raise ValueError
    except IndexError:
        server_adr = DEF_IP_ADR
        server_port = DEF_PORT
    except ValueError:
        print('Порт должен быть в диапазоне от 1024 до 65535')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_adr, server_port))

    message_to_server = create_presence()
    send_message(transport, message_to_server)

    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение от сервера')


if __name__ == '__main__':
    main()
