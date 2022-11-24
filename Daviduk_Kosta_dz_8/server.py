from socket import *
import json
import sys
import argparse
from my_func import js_dec, js_enc

import time

import select

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


def pars_listen(data, messages, client):
    if data['action'] == 'presence':
        LOG.info(f'"OK" ответ сервера клиенту "{client.fileno()}"')
        client.send(js_enc({'response': 200}, USER))
        return
    if data['action'] == 'msg':
        messages.append(data["message"])
        LOG.debug(f'Помечаем сообщение от пользователя "{client.fileno()}", как ВАЖНОЕ УВЕДОМЛЕНИЕ:\n{messages} ')
        return
    else:
        LOG.info(f'"BAD" ответ сервера клиенту "{client.fileno()}"')
        return {
            'response': 400,
            'alert': 'Bad Request'
        }


def read_clients(r, clients):
    """ Чтение запросов из списка клиентов
        """
    messages = []
    for call in r:
        try:
            listen = js_dec(call.recv(1024), USER)
            LOG.debug(f'Получено сообщение от пользователя "{call.fileno()}":\n{listen} ')
            pars_listen(listen, messages, call)
        except:
            LOG.info(f'Клиент "{call.fileno()}", {call.getpeername()} отключился')
            clients.remove(call)
    return messages


def write_clients(requests, w, clients):
    """ Ответ сервера клиентам, от которых были запросы
        """
    for call in w:
        message_dict = {
            "action": "msg",
            "message": requests[0]
        }
        try:
            LOG.info(f'Отправляем ВАЖНОЕ УВЕДОМЛЕНИЕ пользователю "{call.fileno()}":\n{message_dict}')
            call.send(js_enc(message_dict, USER))
        except:
            LOG.info(f'Клиент "{call.fileno()}", {call.getpeername()} отключился')
            call.close()
            clients.remove(call)


def main():
    LOG.debug('"Старт сервера"')
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    port = namespace.port
    address = namespace.addr

    if not 1023 < port < 65536:
        LOG.critical(f'Недопустимый порт "{port}". Допустимы порты с 1024 до 65535.')
        sys.exit(1)

    LOG.info(f'Порт для подключений: "{port}". Адрес подключения: "{address}"')

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((address, port))
    s.listen(5)

    s.settimeout(0.2)
    clients = []

    while True:
        try:
            conn, addr = s.accept()
        except OSError as e:
            pass
        else:
            LOG.info(f'Соединение с клиентом "{conn.fileno()}", {conn.getpeername()}')
            clients.append(conn)
        finally:
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], 0)
            except:
                pass

            requests = read_clients(r, clients)

            if requests and w:
                write_clients(requests, w, clients)


if __name__ == '__main__':
    main()
