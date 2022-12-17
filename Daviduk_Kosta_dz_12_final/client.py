from socket import *
import json
import time
import sys
import argparse
from my_func import js_dec, js_enc
import logging
from client_d_b import ClientBase

import threading
import log.client_log_config
from client_oop import Recept, Send

# python3 client.py
# python3 client.py 127.0.0.8 10000

USER = 'client'

LOG = logging.getLogger('client')


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', nargs='?', default='127.0.0.1')
    parser.add_argument('port', nargs='?', type=int, default=7777)
    return parser


def pars_listen(data):
    if data['response'] == 200:
        return 'response: 200'
    return 'response: 400'


def online(name):
    return {
        "action": "presence",
        "time": int(time.time()),
        "type": "status",
        "user": {
            "account_name": name
        }
    }


def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    port = namespace.port
    address = namespace.addr

    LOG.debug('"Запущен клиент"')

    if not 1023 < port < 65536:
        LOG.critical(f'Недопустимый порт "{port}". Допустимы порты с 1024 до 65535.')
        sys.exit(1)

    user = input('Введите login: ')
    if user == '':
        user = 'visitor'

    LOG.info(f'Порт сервера: "{port}". Адрес сервера: "{address}". login: {user}')
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((address, port))

        msg = online(user)
        s.send(js_enc(msg, USER))
        listen = js_dec(s.recv(1024), USER)
        LOG.info(f'Ответ сервера: "{pars_listen(listen)}"')
    except json.JSONDecodeError as e:
        LOG.error(f'Не удалось декодировать полученную Json строку: {e}')
    except ConnectionRefusedError as e1:
        LOG.critical(f'Не удалось подключиться к серверу {address}:{port}: {e1}')
    else:
        db = ClientBase()
        recept = Recept(s, address, port, user, db)
        recept.daemon = True
        recept.start()
        LOG.debug('Поток на прием')
        send = Send(s, address, port, user, db)
        send.daemon = True
        send.start()
        LOG.debug('Поток на отправку')

    while True:
        time.sleep(1)
        if recept.is_alive() and send.is_alive():
            continue
        break


if __name__ == '__main__':
    main()
