import logging.handlers
import os

from Lesson_5.common.variables import LOGGING_LEVEL

PATH = os.path.dirname(__file__)[0:40]
PATH = os.path.join(PATH, 'logfiles\\server.log')

FORMATTER_SERVER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
LOG_FILE.setFormatter(FORMATTER_SERVER)

LOGGER = logging.getLogger('server')
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)
