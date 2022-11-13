from socket import *
import json
import sys
import argparse
from my_func import js_dec, js_enc

import logging
import log.server_log_config

# python3 server.py
# python3 server.py -p 10000 -a 127.0.0.8

USER = 'server'

LOG = logging.getLogger('server')


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=7777)
    parser.add_argument('-a', '--addr', default='127.0.0.1')
    return parser


def pars_listen(data):
    if data['action'] == 'presence':
        return {
            'response': 200,
            'alert': 'OK'
        }
    return {
        'response': 400,
        'alert': 'Bad Request'
    }


def main():
    LOG.debug('Старт сервера')
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    port = namespace.port
    address = namespace.addr

    if not 1023 < port < 65536:
        LOG.critical(f'Недопустимый порт {port}. Допустимы порты с 1024 до 65535.')
        sys.exit(1)

    LOG.info(f'Порт для подключений: {port}. Адрес подключения: {address}')

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((address, port))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        LOG.info(f'Получаем запрос на соединение: {addr}')
        # print('Получаем запрос на соединение:', addr)
        try:
            listen = js_dec(conn.recv(1024), USER)
            LOG.debug(f'Получено сообщение : {listen}')
            # print(listen)
            reply = pars_listen(listen)
            LOG.info(f'Ответ клиенту: {reply}')
            conn.send(js_enc(reply, USER))
            LOG.debug(f'Соединение с клиентом {addr} закрывается.')
            conn.close()
        except json.JSONDecodeError as e:
            LOG.error(f'Не удалось декодировать полученную Json строку: {e}')
            LOG.debug(f'Соединение с клиентом {addr} закрывается.')
            conn.close()


if __name__ == '__main__':
    main()
