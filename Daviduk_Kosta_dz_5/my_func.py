import json
import logging
import log.server_log_config

log_server = logging.getLogger('server')
log_client = logging.getLogger('client')


def js_dec(data, user):
    if user == 'server':
        log_server.debug(f'Декодируем сообщение: {data}')
    elif user == 'client':
        log_client.debug(f'Декодируем сообщение: {data}')
    dec_data = data.decode('utf-8')
    js_data = json.loads(dec_data)
    return js_data


def js_enc(data, user):
    if user == 'server':
        log_server.debug(f'Кодируем сообщение: {data}')
    elif user == 'client':
        log_client.debug(f'Кодируем сообщение: {data}')
    js_data = json.dumps(data)
    enc_data = js_data.encode('utf-8')
    return enc_data
