import json
import logging
import log.server_log_config
import log.client_log_config
from wrapper import Log

log_server = logging.getLogger('server')
log_client = logging.getLogger('client')


@Log()
def js_dec(data, user):
    """ Чтение JSON-файла """
    if user == 'server':
        log_server.debug(f'Функция декодирует сообщение серверу')
    elif user == 'client':
        log_client.debug(f'Функция декодирует сообщение пользователю')
    dec_data = data.decode('utf-8')
    js_data = json.loads(dec_data)
    return js_data


@Log()
def js_enc(data, user):
    """ Запись в JSON-файл """
    if user == 'server':
        log_server.debug(f'Функция кодирует сообщение серверу')
    elif user == 'client':
        log_client.debug(f'Функция кодирует сообщение пользователю')
    js_data = json.dumps(data)
    enc_data = js_data.encode('utf-8')
    return enc_data
