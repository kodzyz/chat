import threading
import logging
import sys
import json
from meta import ClientVerifier
import time

LOG = logging.getLogger('client')


class Message(threading.Thread, metaclass=ClientVerifier):
    def __init__(self, socket, address, port, login, database):
        self.s = socket
        self.addr = address
        self.port = port
        self.login = login
        self.database = database
        super().__init__()


class Recept(Message):

    def __init__(self, socket, address, port, login, database):
        super().__init__(socket, address, port, login, database)

    def run(self):
        """Режим приема сообщений"""
        while True:
            try:
                data = self.js_dec(self.s.recv(1024))
                if "to" in data and data["to"] == '#' and "message" in data and "from" in data:
                    LOG.info(f'Прием - "{data["from"]}" принял "{data["message"]}"')
                    print(f'Принято сообщение от {data["from"]}:\n"{data["message"]}"')
                elif "to" in data and data["to"] == self.login and "message" in data and "from" in data:
                    LOG.info(f'Прием - "{data["to"]}" принял от "{data["from"]}":\n{data["message"]}')
                    print(f'Принято сообщение от {data["from"]}:\n"{data["message"]}"')
                elif 'response' in data and data['response'] == 202 and "alert" in data:
                    print(f'Список контактов: "{data["alert"]}"')
                    LOG.info(f'Список контактов: "{data["alert"]}"')

                elif 'response' in data and data['response'] == 201 and "alert" in data:
                    print(f'{data["alert"]}')
                    LOG.info(f'{data["alert"]}')

                elif 'response' in data and data['response'] == 203 and "alert" in data:
                    print(f'{data["alert"]}')
                    LOG.info(f'{data["alert"]}')

                else:
                    LOG.info(f'Прием - Получено некорректное сообщение: {data}')
            except:
                LOG.error(f'Прием - Нет соединение с сервером "{self.addr}:{self.port}".')
                break

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
        return js_data


class Send(Message):
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

    def message_(self, notice, receiver):
        return {
            "action": "message",
            "time": int(time.time()),
            "from": self.login,
            "to": receiver,
            "message": notice
        }

    def add_contact_(self, nickname, login):
        return {
            "action": "add_contact",
            "user_id": nickname,
            "time": int(time.time()),
            "user_login": login
        }

    def del_contact_(self, nickname, login):
        return {
            "action": "del_contact",
            "user_id": nickname,
            "time": int(time.time()),
            "user_login": login
        }

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
                self.s.send(self.js_enc(self.contacts_(self.login)))
                LOG.info(f'Отправка - Получение списка контактов: {self.contacts_(self.login)}')

            elif mes == "add_contact":
                add_contact = input('Имя контакта для добавления в список контактов: ')
                self.s.send(self.js_enc(self.add_contact_(add_contact, self.login)))
                LOG.info(f'Отправка - Добавление контакта в список контактов: {self.add_contact_(add_contact, self.login)}')

            elif mes == "del_contact":
                del_contact = input('Имя контакта для удаления из списка контактов: ')
                self.s.send(self.js_enc(self.del_contact_(del_contact, self.login)))
                LOG.info(f'Отправка - Удаление контакта из списка контактов: {self.del_contact_(del_contact, self.login)}')

            elif mes == "see_messages":
                recipient = input('Имя контакта для отображения переписки: ')
                see_messages = self.database.see_messages(sender=self.login, recipient=recipient)
                for messages in see_messages:
                    print(messages)
                LOG.info(f'Отправка - Переписка между "{self.login}" и "{recipient}":\n{see_messages}')

            else:
                whom_to = input('Введите "login" получателя(# - всем): ')

                try:
                    LOG.info(f'Отправка - "{self.login}" пишет "{whom_to}": {self.message_(mes, whom_to)}')
                    self.s.send(self.js_enc(self.message_(mes, whom_to)))
                    self.database.save_message(self.login, whom_to, mes)

                except:
                    LOG.error(f'Отправка - Нет соединение с сервером {self.addr}:{self.port}.')
                    exit(1)

    @staticmethod
    def js_enc(data):
        """ Запись в JSON-файл """
        LOG.debug(f'JSON - кодирует сообщение пользователю')
        js_data = json.dumps(data)
        enc_data = js_data.encode('utf-8')
        return enc_data
