import logging
import sys
import json
from socket import *
import select
from meta import ServerVerifier
import log.server_log_config

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


class Server(metaclass=ServerVerifier):
    port = Port()

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.clients = []
        self.s = socket(AF_INET, SOCK_STREAM)

    def start(self):
        LOG.info(f'Порт для подключений: "{self.port}". Адрес подключения: "{self.address}"')
        # s = socket(AF_INET, SOCK_STREAM)
        self.s.bind((self.address, self.port))
        self.s.listen(5)
        self.s.settimeout(0.2)

        while True:
            try:
                conn, addr = self.s.accept()
            except OSError as e:
                pass
            else:
                LOG.info(f'Соединение с клиентом "{conn.fileno()}", {conn.getpeername()}')
                self.clients.append(conn)
            finally:
                r = []
                w = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], 0)
                except:
                    pass

                requests = self.read_clients(r, self.clients)

                if requests and w:
                    self.write_clients(requests, w, self.clients)

    def read_clients(self, r, clients):
        """ Чтение запросов из списка клиентов
                """
        messages = []
        for call in r:
            try:
                listen = self.js_dec(call.recv(1024))
                LOG.debug(f'Получено сообщение от пользователя "{call.fileno()}":\n{listen} ')
                self.pars_listen(listen, messages, call)
            except:
                LOG.info(f'Клиент "{call.fileno()}", {call.getpeername()} отключился')
                clients.remove(call)
        return messages

    def write_clients(self, requests, w, clients):
        """ Ответ сервера клиентам, от которых были запросы
                """
        for call in w:
            message_dict = {
                "action": "msg",
                "message": requests[0]
            }
            try:
                LOG.info(f'Отправляем ВАЖНОЕ УВЕДОМЛЕНИЕ пользователю "{call.fileno()}":\n{message_dict}')
                call.send(self.js_enc(message_dict))
            except:
                LOG.info(f'Клиент "{call.fileno()}", {call.getpeername()} отключился')
                call.close()
                clients.remove(call)

    def pars_listen(self, data, messages, client):
        if data['action'] == 'presence':
            LOG.info(f'"OK" ответ сервера клиенту "{client.fileno()}"')
            client.send(self.js_enc({'response': 200}))
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

    @staticmethod
    def js_dec(data):
        """ Чтение JSON-файла """
        LOG.debug(f'Функция декодирует сообщение серверу')
        dec_data = data.decode('utf-8')
        js_data = json.loads(dec_data)
        return js_data

    @staticmethod
    def js_enc(data):
        """ Запись в JSON-файл """
        LOG.debug(f'Функция декодирует сообщение серверу')
        js_data = json.dumps(data)
        enc_data = js_data.encode('utf-8')
        return enc_data


p = Server(45, 6553)
# print(p.__dict__)  # {'address': 45, '_port': 6553}
# p = Server(45, 0)
# print(p.__dict__)  # Недопустимый порт "0". Допустимы порты с 1024 до 65535.
