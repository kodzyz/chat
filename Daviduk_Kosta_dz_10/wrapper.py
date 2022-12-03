import inspect
from functools import wraps
import logging
import log.wrapp_log_config

log_wrapp_server = logging.getLogger('wrapp_server')
log_wrapp_client = logging.getLogger('wrapp_client')


class Log:

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            mess = (f'Функция: {func.__name__}({args}, {kwargs})',
                    f'Вызвана из функции: "{inspect.stack()[1][3]}"')

            if args[1] == 'server':
                log_wrapp_server.info(wrapper.__doc__)
                log_wrapp_server.debug(mess)
            if args[1] == 'client':
                log_wrapp_client.info(wrapper.__doc__)
                log_wrapp_client.debug(mess)

            res = func(*args, **kwargs)

            return res

        return wrapper
