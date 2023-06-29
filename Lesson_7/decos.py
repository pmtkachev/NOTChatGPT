from logging import getLogger
import sys
from inspect import stack

if sys.argv[0].find('client') == -1:
    LOGGER = getLogger('server')
else:
    LOGGER = getLogger('client')


def log(func):
    def log_save(*args, **kwargs):
        logsave = func(*args, **kwargs)
        LOGGER.debug(
            f'Вызвана функция {func.__name__} с параметрами {args}, {kwargs}'
            f' из модуля {func.__module__}. '
            f'Из функции {stack()[1][3]}.', stacklevel=2)
        return logsave

    return log_save
