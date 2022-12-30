import threading
import logging
import sys
import json

from PyQt5.QtCore import pyqtSignal, QObject
from meta import ClientVerifier
import time

LOG = logging.getLogger('client')
sock_lock = threading.Lock()
database_lock = threading.Lock()


class Message(threading.Thread):
    def __init__(self, socket, address, port, login, database):
        self.s = socket
        self.addr = address
        self.port = port
        self.login = login
        self.database = database
        self.contact_list = ''
        self.public_key = None
        super().__init__()


class Recept(Message, QObject):
    '''
    Класс реализующий транспортную подсистему клиентского
    модуля. Отвечает за прием сообщений с сервера.
    '''
    # Сигнал новое сообщение
    new_message = pyqtSignal(dict)

    def __init__(self, socket, address, port, login, database):
        super().__init__(socket, address, port, login, database)
        QObject.__init__(self)

    def run(self):
        """Режим приема сообщений"""
        while True:
            time.sleep(1)

            # try:
            data = self.js_dec(self.s.recv(1024))
            if "to" in data and data["to"] == '#' and "message" in data and "from" in data:
                LOG.info(f'Прием - "{data["from"]}" принял "{data["message"]}"')
                print(f'Принято сообщение от {data["from"]}:\n"{data["message"]}"')

            elif "to" in data and data["to"] == self.login and "message" in data and "from" in data:
                LOG.info(f'Прием - "{data["to"]}" принял от "{data["from"]}":\n{data["message"]}')
                # print(f'Принято сообщение от {data["from"]}:\n"{data["message"]}"')
                self.new_message.emit(data)

            elif 'response' in data and data['response'] == 202 and "alert" in data:
                if data["alert"] == 400:
                    print('Список контактов пуст')
                else:
                    print(f'Список контактов: "{data["alert"]}"')
                    LOG.info(f'Список контактов: "{data["alert"]}"')
                    self.contact_list = data["alert"]
                    # print(f'client1 = {self.contact_list}, {type(self.contact_list)}')
                    # self.contact_list.split(',')
            elif 'response' in data and data['response'] == 201 and "alert" in data:
                print(f'{data["alert"]}')
                LOG.info(f'{data["alert"]}')

            elif 'response' in data and data['response'] == 203 and "alert" in data:
                print(f'{data["alert"]}')
                LOG.info(f'{data["alert"]}')

            elif 'response' in data and data['response'] == 512:
                # print(f'Прием - Публичный ключ с сервера: {data["alert"]}')
                # LOG.info(f'публичный ключ {data["alert"]}')
                self.key_reply(data["alert"])


            else:
                LOG.info(f'Прием - Получено некорректное сообщение: {data}')
            # except:
            #     LOG.error(f'Прием - Нет соединение с сервером "{self.addr}:{self.port}".')
            #     break

    def key_reply(self, data):
        '''Публичный ключ с сервера'''
        self.public_key = data
        # print(f'client_oop - def key_reply: self.public_rey: {self.public_key}')

    @staticmethod
    def pars_from_server(data):
        if data['action'] == 'message':
            response = data['message']
            return response
        return 'response: 400'

    @staticmethod
    def js_dec(data):
        """ Чтение JSON-файла """
        LOG.debug(f'JSON - декодирует сообщение от пользователя')
        dec_data = data.decode('utf-8')
        js_data = json.loads(dec_data)
        if isinstance(js_data, dict):
            return js_data
        else:
            LOG.error(f'JSON - некорректное сообщение')
            return


class Send(Message):
    '''
    Класс реализующий транспортную подсистему клиентского
    модуля. Отвечает за отправку сообщений на сервер.
    '''

    def __init__(self, socket, address, port, login, database):
        super().__init__(socket, address, port, login, database)

    def exit_(self, name):
        return {
            "action": "exit",
            "time": int(time.time()),
            "account_name": name
        }

    def contacts_(self, name):
        return {
            "action": "get_contacts",
            "time": int(time.time()),
            "user_login": name
        }

    def contacts(self):
        '''Получение списка контактов'''
        with sock_lock:
            self.s.send(self.js_enc(self.contacts_(self.login)))
            LOG.info(f'Отправка - Получение списка контактов: {self.contacts_(self.login)}')

    def message_(self, notice, receiver):
        return {
            "action": "message",
            "time": int(time.time()),
            "from": self.login,
            "to": receiver,
            "message": notice
        }

    def send_message(self, message, receiving):
        '''Отправка сообщения'''
        with sock_lock:
            self.s.send(self.js_enc(self.message_(message, receiving)))
            # self.database.save_message(self.login, receiving, message)
            LOG.info(f'Отправка - "{self.login}" пишет "{receiving}": {self.message_(message, receiving)}')

    def add_contact_(self, nickname, login):
        return {
            "action": "add_contact",
            "user_id": nickname,
            "time": int(time.time()),
            "user_login": login
        }

    def add_contact(self, add_contact):
        '''Добавление контакта в список контактов'''
        with sock_lock:
            self.s.send(self.js_enc(self.add_contact_(add_contact, self.login)))
            LOG.info(f'Отправка - Добавление контакта в список контактов: {self.add_contact_(add_contact, self.login)}')

    def del_contact_(self, nickname, login):
        return {
            "action": "del_contact",
            "user_id": nickname,
            "time": int(time.time()),
            "user_login": login
        }

    def del_contact(self, del_contact):
        '''Удаление контакта из списка контактов'''
        with sock_lock:
            self.s.send(self.js_enc(self.del_contact_(del_contact, self.login)))
            LOG.info(
                f'Отправка - Удаление контакта из списка контактов: {self.del_contact_(del_contact, self.login)}')

    def history_message(self, recipient):
        a_ = []
        see_messages = self.database.see_messages(sender=self.login, recipient=recipient)
        # print(f'history_message: {see_messages}')
        for i in see_messages:
            for j in range(len(i)):
                a_.append(i[j][3])
                # print(i[j][3])
        return a_

    def key_request_(self, name):
        return {
            "action": "pubkey",
            "time": int(time.time()),
            "user_login": name
        }

    def key_request(self, name):
        '''Запрос публичного ключа'''
        # LOG.info(f'Запрос публичного ключа для {name}')
        # print(f'"def key_request" - Запрос публичного ключа для {name}')
        with sock_lock:
            self.s.send(self.js_enc(self.key_request_(name)))
            # LOG.info(f'Отправка - Запрос публичного ключа: {self.key_request_(name)}')
            # print(f'"def key_request" - Запрос публичного ключа: {self.key_request_(name)}')

    def run(self):
        """Режим отправки сообщений"""
        while True:

            mes = input('Ваше сообщение: ')
            if mes == 'exit':
                self.s.send(self.js_enc(self.exit_(self.login)))
                LOG.info(f'Отправка - "EXIT {self.login}": {self.exit_(self.login)}')
                time.sleep(0.5)
                sys.exit(1)

            elif mes == "get_contacts":
                # self.s.send(self.js_enc(self.contacts_(self.login)))
                # LOG.info(f'Отправка - Получение списка контактов: {self.contacts_(self.login)}')
                self.contacts()

            elif mes == "add_contact":
                name = input('Имя контакта для добавления в список контактов: ')
                # self.s.send(self.js_enc(self.add_contact_(add_contact, self.login)))
                # LOG.info(f'Отправка - Добавление контакта в список контактов: {self.add_contact_(add_contact, self.login)}')
                self.add_contact(name)

            elif mes == "del_contact":
                name = input('Имя контакта для удаления из списка контактов: ')
                # self.s.send(self.js_enc(self.del_contact_(del_contact, self.login)))
                # LOG.info(
                #     f'Отправка - Удаление контакта из списка контактов: {self.del_contact_(del_contact, self.login)}')
                self.del_contact(name)

            elif mes == "see_messages":
                recipient = input('Имя контакта для отображения переписки: ')
                see_messages = self.history_message(recipient)
                for messages in see_messages:
                    print(messages)
                LOG.info(f'Отправка - Переписка между "{self.login}" и "{recipient}":\n{see_messages}')

            elif mes == "key_public":
                self.key_request()

            else:
                whom_to = input('Введите "login" получателя(# - всем): ')

                # try:
                self.send_message(mes, whom_to)

                # except:
                #     LOG.error(f'Отправка - Нет соединение с сервером {self.addr}:{self.port}.')
                #     exit(1)

    @staticmethod
    def js_enc(data):
        """ Запись в JSON-файл """
        LOG.debug(f'JSON - кодирует сообщение пользователю')
        js_data = json.dumps(data)
        enc_data = js_data.encode('utf-8')
        return enc_data
