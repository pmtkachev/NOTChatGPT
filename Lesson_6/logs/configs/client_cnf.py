import logging.handlers
import os
from Lesson_5.common.variables import LOGGING_LEVEL

PATH = os.path.dirname(__file__)[0:40]
PATH = os.path.join(PATH, 'logfiles\\client.log')

FORMATTER_CLIENT = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')
LOG_FILE = logging.FileHandler(PATH, encoding='utf8')
LOG_FILE.setFormatter(FORMATTER_CLIENT)

LOGGER = logging.getLogger('client')
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)
