import binascii
from socket import *
import json
import time
import sys
import argparse
from my_func import js_dec, js_enc
import logging
from client_d_b import ClientBase
from PyQt5.QtWidgets import QApplication
import threading
import log.client_log_config
from client_oop import Recept, Send
from client.start_dialog import UserNameDialog
from client.main_window import ClientMainWindow
import os
import hmac

from Cryptodome.PublicKey import RSA

# python3 client.py
# python3 client.py 127.0.0.8 10000

USER = 'client'

LOG = logging.getLogger('client')
secret_key = b'our_secret_key'


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', nargs='?', default='127.0.0.1')
    parser.add_argument('port', nargs='?', type=int, default=7777)
    return parser


def pars_listen(data):
    if data['response'] == 200:
        return 'response: 200'
    return 'response: 400'


def online(name, keys):
    # Получаем публичный ключ и декодируем его из байтов
    pubkey = keys.publickey().export_key().decode('ascii')
    return {
        "action": "presence",
        "time": int(time.time()),
        "type": "status",
        "user": {
            "account_name": name
        },
        "pubkey": pubkey
    }


def online_auth(response):
    return {
        'response': 511,
        "alert": response.decode('ascii')
    }


def client_authenticate(conn):
    """
        Аутентификация клиента на удаленном сервисе.
        Параметр connection - сетевое соединение (сокет)
        secret_key - ключ шифрования, известный клиенту и серверу
        """
    # принимаем случайное послание от сервера
    listen = js_dec(conn.recv(1024), USER)
    if 'response' in listen and listen['response'] == 400:
        LOG.info('Пользователь не зарегистрирован.')
        raise 'Пользователь не зарегистрирован.'
    elif listen['response'] == 511:
        random_message = listen["alert"].encode('ascii')
        # Вычисляется HMAC-функция
        hash = hmac.new(secret_key, random_message, 'MD5')
        digest = hash.digest()
        response = binascii.b2a_base64(digest)
        LOG.debug(f'Авторизация - HMAC-функция клиент = {response}')
        # отправляем ответ серверу
        msg = online_auth(response)
        conn.send(js_enc(msg, USER))


def keys_message(name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # print(dir_path)
    key_file = os.path.join(dir_path, f'{name}.key')
    # print(key_file)
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())
    return keys


def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    port = namespace.port
    address = namespace.addr

    LOG.debug('"Запущен клиент"')

    if not 1023 < port < 65536:
        LOG.critical(f'Недопустимый порт "{port}". Допустимы порты с 1024 до 65535.')
        sys.exit(1)

    # Создаём клиентокое приложение
    client_app = QApplication(sys.argv)
    start_dialog = UserNameDialog()
    client_app.exec_()
    # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое и удаляем объект, инааче выходим
    if start_dialog.ok_pressed:
        user = start_dialog.client_name.text()
        password = start_dialog.client_passwd.text()
        del start_dialog
    else:
        exit(0)

    LOG.info(f'Порт сервера: "{port}". Адрес сервера: "{address}", login: {user}, passwd: {password}')

    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((address, port))

        # Загружаем ключи с файла, если же файла нет, то генерируем новую пару.
        keys = keys_message(user)

        # Авторизируемся на сервере
        msg = online(user, keys)
        s.send(js_enc(msg, USER))

        # Запускаем процедуру авторизации
        client_authenticate(s)

        listen = js_dec(s.recv(1024), USER)
        LOG.info(f'Ответ сервера: "{pars_listen(listen)}"')
    except json.JSONDecodeError as e:
        LOG.error(f'Не удалось декодировать полученную Json строку: {e}')
    except ConnectionRefusedError as e1:
        LOG.critical(f'Не удалось подключиться к серверу {address}:{port}: {e1}')
    else:
        # Создаём объект базы данных
        db_client = ClientBase()
        recept = Recept(s, address, port, user, db_client)
        recept.daemon = True
        recept.start()
        LOG.debug('Поток на прием')
        send = Send(s, address, port, user, db_client)
        send.daemon = True
        send.start()
        LOG.debug('Поток на отправку')

        # Создаём GUI
        main_window = ClientMainWindow(db_client, recept, send, user, keys)
        main_window.setWindowTitle(f'Чат "{user}"')
        client_app.exec_()

    while True:
        time.sleep(1)
        if recept.is_alive() and send.is_alive():
            continue
        break


if __name__ == '__main__':
    main()
