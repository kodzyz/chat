import threading
import logging
import sys
import json
from meta import ClientVerifier

LOG = logging.getLogger('client')


class Message(threading.Thread, metaclass=ClientVerifier):
    def __init__(self, socket, address, port):
        self.s = socket
        self.addr = address
        self.port = port
        super().__init__()


class Recept(Message):

    def __init__(self, socket, address, port):
        super().__init__(socket, address, port)

    def run(self):
        """Режим приема сообщений"""
        while True:
            try:
                data = self.js_dec(self.s.recv(1024))
                LOG.info(f'Принято:\n"{self.pars_from_server(data)}"')
                print(
                    f'Принято:\n"{self.pars_from_server(data)}"')
            except:
                LOG.error(f'Нет соединение с сервером "{self.addr}:{self.port}".')
                sys.exit(1)

    @staticmethod
    def pars_from_server(data):
        if data['action'] == 'msg':
            response = data['message']
            return response
        return 'response: 400'

    @staticmethod
    def js_dec(data):
        """ Чтение JSON-файла """
        LOG.debug(f'Функция декодирует сообщение пользователю')
        dec_data = data.decode('utf-8')
        js_data = json.loads(dec_data)
        return js_data


class Send(Message):
    def __init__(self, socket, address, port):
        super().__init__(socket, address, port)

    def run(self):
        """Режим отправки сообщений"""
        while True:
            try:
                mes = input('Ваше сообщение: ')
                if mes == 'exit':
                    LOG.error(f'Клиент "{self.s.fileno()}", {self.s.getpeername()} отключился')
                    sys.exit(1)
                message_dict = {
                    "action": "msg",
                    "message": mes
                }
                self.s.send(self.js_enc(message_dict))
                LOG.info(f'Отправляем ВАЖНОЕ УВЕДОМЛЕНИЕ пользователям:\n{message_dict}')
            except:
                LOG.error(f'Нет соединение с сервером {self.addr}:{self.port}.')
                sys.exit(1)

    @staticmethod
    def js_enc(data):
        """ Запись в JSON-файл """
        LOG.debug(f'Функция кодирует сообщение пользователю')
        js_data = json.dumps(data)
        enc_data = js_data.encode('utf-8')
        return enc_data
