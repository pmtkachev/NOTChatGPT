"""Константы"""

import logging

# Порт и IP адрес по умолчанию
DEF_PORT = 7777
DEF_IP_ADR = '127.0.0.1'

# Максимальная очередь подключений
MAX_CON = 5

# Максимальная длина сообщения
MAX_PACK_LEN = 1024

# Кодировка
ENCODING = 'utf-8'

# Протокол JIM основные ключи
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACC_NAME = 'account_name'

SENDER = 'sender'

# Прочие ключи
MESSAGE = 'message'
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESS_TEXT = 'mess_text'
EXIT = 'exit'
DEST = 'to'
RESP_200 = {RESPONSE: 200}
RESP_400 = {
    RESPONSE: 400,
    ERROR: None
}

# Уровень логгера
LOGGING_LEVEL = logging.DEBUG
