import logging
import sys
import json
import threading
from socket import *
import select
import os
import binascii
import hmac
from meta import ServerVerifier
import log.server_log_config
import time

LOG = logging.getLogger('server')


class Port:
    @classmethod
    def verify_port(cls, port):
        if not 1023 < port < 65536:
            LOG.critical(f'Недопустимый порт "{port}". Допустимы порты с 1024 до 65535.')
            sys.exit(1)

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        self.verify_port(value)
        setattr(instance, self.name, value)


class Server(threading.Thread):
    '''
    Основной класс сервера. Принимает содинения, словари - пакеты
    от клиентов, обрабатывает поступающие сообщения.
    Работает в качестве отдельного потока.
    '''
    port = Port()

    def __init__(self, address, port, database):
        self.address = address
        self.port = port
        self.clients = []  # очередь клиентов
        self.s = socket(AF_INET, SOCK_STREAM)
        self.messages = []  # очередь сообщений
        self.login = dict()  # {login: socket}
        self.database = database
        # Конструктор предка
        super().__init__()

    def run(self):
        '''Метод основной цикл потока.'''
        LOG.info(f'Запуск - Порт: "{self.port}". Адрес: "{self.address}"')
        self.s.bind((self.address, self.port))
        self.s.listen(5)
        self.s.settimeout(0.2)

        while True:
            try:
                conn, addr = self.s.accept()
            except OSError as e:
                pass
            else:
                LOG.info(f'Запуск - Соединение по адресу "{addr}"')
                self.clients.append(conn)
            finally:
                r = []
                w = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], 0)
                except OSError:
                    pass
                self.read_clients(r)
                if self.messages and w:
                    self.write_clients(w)

    def read_clients(self, r):
        '''Чтение запросов из списка клиентов'''
        if r:
            for call in r:
                #try:
                listen = self.js_dec(call.recv(1024))
                LOG.debug(f'Чтение запросов - Получено сообщение: {listen}')
                self.pars_listen(listen, call)
                # except:
                #     LOG.info(f'Чтение запросов - {call.getpeername()} отключился')
                #     self.clients.remove(call)

    def write_clients(self, w):
        '''Ответ сервера клиентам, от которых были запросы'''
        for data in self.messages:
            LOG.info('write_clients')
            try:
                if data["to"] == '#':  # всем
                    for call in w:
                        LOG.info(f'Ответ сервера - "{data["from"]}" пишет всем: {data["message"]}')
                        call.send(self.js_enc(data))

                elif self.login[data["to"]] in w and data["to"] in self.login:  #  and data["to"] != '#'
                    LOG.info(f'Ответ сервера - "{data["from"]}" пишет "{data["to"]}": {data}')
                    self.login[data["to"]].send(self.js_enc(data))
            except:
                LOG.error(f'Ответ сервера - Клиент "{data["from"]}" не найден')
                self.clients.remove(self.login[data["to"]])
                del self.login[data["to"]]
        self.messages[:] = []

    def autorize_user(self, data, client):
        '''Авторизация пользователей.'''
        secret_key = b'our_secret_key'
        LOG.info(f'Авторизация - "Начало" "{data["user"]["account_name"]}"')
        # Проверяем что пользователь зарегистрирован на сервере.
        if not self.database.check_client(data["user"]["account_name"]):
            LOG.info(f'Авторизация - "{data["user"]["account_name"]}" не зарегистрирован.')
            client.send(self.js_enc({'response': 400}))
            self.clients.remove(client)
            client.close()
        else:
            LOG.info(f'Авторизация - "{data["user"]["account_name"]}" зарегистрирован.')
            # проводим процедуру авторизации
            # 1. Создаётся случайное послание и отсылается клиенту
            random_message = binascii.hexlify(os.urandom(64))
            client.send(self.js_enc(
                {
                    'response': 511,
                    "alert": random_message.decode('ascii')
                }
            ))
            # print(f'Авторизация - random_message = {random_message.decode("ascii")}')
            LOG.debug(f'Авторизация - random_message = {random_message.decode("ascii")}')
            # 2. Вычисляется HMAC-функция
            hash = hmac.new(secret_key, random_message, 'MD5')
            digest = hash.digest()
            # print(f'Авторизация digest= {digest}')
            LOG.debug(f'Авторизация - HMAC-функция сервер = {digest}')
            # 3. Пришедший ответ от клиента сравнивается с локальным результатом HMAC
            response = self.js_dec(client.recv(1024))
            digest2 = binascii.a2b_base64(response["alert"])
            # print(f'Авторизация response= {digest2}')
            LOG.debug(f'Авторизация - HMAC-функция клиент = {digest2}')
            LOG.debug(f'Авторизация - HMAC-сравнение = {hmac.compare_digest(digest, digest2)}')
            return hmac.compare_digest(digest, digest2)

    def pars_listen(self, data, client):
        """Обработчик сообщений """
        if 'action' in data and data['action'] == 'presence':
            if data["user"]["account_name"] not in self.login.keys():
                # Если сообщение о присутствии то вызываем функцию авторизации.
                if not self.autorize_user(data, client):
                    # self.clients.remove(client)
                    # client.close()
                    print('Обработчик сообщений - "if not autorize_user"')
                    return
                # print("Авторизация успех")
                LOG.info("Авторизация успех")
                self.login[data["user"]["account_name"]] = client  # {'ko': 1}
                client_ip, client_port = client.getpeername()
                self.database.save_log(data["user"]["account_name"], client_ip, data["pubkey"])
                LOG.info(f'Обработчик - "OK" ответ сервера клиенту "{data["user"]["account_name"]}"')
                client.send(self.js_enc({'response': 200}))
            else:
                LOG.info('Обработчик - Такой "login" существует.')
                client.send(self.js_enc({'response': 400}))
                self.clients.remove(client)
                client.close()
            return
        elif 'action' in data and data['action'] == 'message':
            LOG.debug(f'Обработчик - Запоминаем сообщение: {data}"')
            self.messages.append(data)
            self.database.messages_db(data["from"], data["to"])
            return
        elif 'action' in data and data['action'] == 'exit':
            LOG.info(f'Обработчик - "exit" clients: {data["account_name"]}')
            self.clients.remove(self.login[data["account_name"]])
            del self.login[data["account_name"]]
            return
        elif 'action' in data and data['action'] == "get_contacts":
            user_login = data['user_login']
            list_client_login = self.database.get_contacts(user_login)
            client.send(self.js_enc(
                {
                    'response': 202,
                    "alert": list_client_login
                }
            ))
            LOG.info(f'Обработчик - Список контактов пользователя "{user_login}": {list_client_login}')
            return
        elif 'action' in data and data['action'] == "add_contact":
            owner = data['user_login']
            add_contact = data['user_id']
            self.database.add_contact(owner, add_contact)
            client.send(self.js_enc(
                {
                    'response': 201,
                    "alert": f"{add_contact} добавлен в список контактов {owner}"
                }
            ))
            LOG.info(f"{add_contact} добавлен в список контактов {owner}")
            return

        elif 'action' in data and data['action'] == "del_contact":
            owner = data['user_login']
            del_contact = data['user_id']
            self.database.del_contact(owner, del_contact)
            client.send(self.js_enc(
                {
                    'response': 203,
                    "alert": f"{del_contact} удален из списка контактов {owner}"
                }
            ))
            LOG.info(f"{del_contact} удален из списка контактов {owner}")
            return

        elif 'action' in data and data['action'] == "pubkey":
            client.send(self.js_enc(
                {
                    'response': 512,
                    "alert": self.database.get_pubkey(data["user_login"])
                }
            ))
            print(f'сервер: "pubkey": {self.database.get_pubkey(data["user_login"])}')

        else:
            LOG.info('Обработчик - Запрос некорректен.')
            client.send(self.js_enc({'response': 400}))
            return

    @staticmethod
    def js_dec(data):
        """ Чтение JSON-файла """
        LOG.debug(f'JSON - декодирует сообщение серверу')
        dec_data = data.decode('utf-8')
        js_data = json.loads(dec_data)
        if isinstance(js_data, dict):
            return js_data
        else:
            LOG.error(f'JSON - некорректное сообщение')
            return

    @staticmethod
    def js_enc(data):
        """ Запись в JSON-файл """
        LOG.debug(f'JSON - кодирует сообщение клиенту')
        js_data = json.dumps(data)
        enc_data = js_data.encode('utf-8')
        return enc_data

# p = Server(45, 6553)
# print(p.__dict__)  # {'address': 45, '_port': 6553}
# p = Server(45, 0)
# print(p.__dict__)  # Недопустимый порт "0". Допустимы порты с 1024 до 65535.
