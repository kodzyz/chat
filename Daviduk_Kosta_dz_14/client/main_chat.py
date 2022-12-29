import base64
import time
import datetime
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox, QApplication, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSlot, QEvent, Qt
import sys
import json
import logging
from client.chat_window import Ui_MainClientWindow

LOG = logging.getLogger('client')


class MainChat(QMainWindow):
    def __init__(self, database_client, send_transport, recept_transport, keys):
        super().__init__()
        # основные переменные
        self.db_client = database_client
        self.recept = recept_transport
        self.send = send_transport

        # объект - дешифорвщик сообщений с предзагруженным ключём
        self.decrypter = PKCS1_OAEP.new(keys)

        # Загружаем конфигурацию окна из дизайнера
        self.ui_chat = Ui_MainClientWindow()
        self.ui_chat.setupUi(self)

        # Кнопка отправить сообщение
        self.ui_chat.btn_send.clicked.connect(self.send_message)

        # Дополнительные требующиеся атрибуты
        self.history_model = None
        self.current_chat = None
        self.encryptor = None
        self.current_chat_key = None

    # Функция устанавливающяя активного собеседника
    def current_receive(self, receive):
        self.current_chat = receive
        self.ui_chat.label_new_message.setText(f'Введите сообщенние для {self.current_chat}:')
        # Заполняем окно историю сообщений по требуемому пользователю
        self.history_list_update()

        # print(f'CHAT - def current_receive: self.current_receive: {self.current_chat}')
        # Запрос публичного ключа
        self.send.key_request(self.current_chat)
        time.sleep(1)
        # Прием - публичного ключа с сервера
        self.current_chat_key = self.recept.public_key
        # print(f'CHAT: Загружен открытый ключ {self.current_chat_key}')
        LOG.debug(f'CHAT: Загружен открытый ключ {self.current_chat_key}')
        if self.current_chat_key:
            self.encryptor = PKCS1_OAEP.new(
                RSA.import_key(self.current_chat_key))

    # Функция отправки собщения пользователю
    def send_message(self):
        # Текст в поле, проверяем что поле не пустое затем забирается сообщение и поле очищается
        message_text = self.ui_chat.text_message.toPlainText()
        self.ui_chat.text_message.clear()
        if not message_text:
            return
        # print(f'"chat" send_message = {message_text}')
        LOG.debug(f'CHAT: сообщение до шифрования - {message_text}')
        # Шифруем сообщение ключом отправителя и упаковываем в base64.
        message_text_encrypted = self.encryptor.encrypt(
            message_text.encode('utf8'))
        message_text_encrypted_base64 = base64.b64encode(
            message_text_encrypted)
        # print(f'chat: send_message_encrypted = {message_text_encrypted_base64.decode("ascii")}')
        LOG.debug(f'CHAT: зашифрованное сообщение для отправки - {message_text_encrypted_base64.decode("ascii")}')
        self.send.send_message(message_text_encrypted_base64.decode('ascii'), self.current_chat)
        # Сохраняем сообщение в базу
        self.db_client.save_message(self.current_chat, 'out', message_text)
        self.history_list_update()

    @pyqtSlot(dict)
    def message_signal(self, message):
        # Получаем строку байтов
        LOG.debug(f'CHAT: принятое сообщение для дешифровки - {message}')
        encrypted_message = base64.b64decode(message["message"])
        decrypted_message = self.decrypter.decrypt(encrypted_message)
        # print(f'chat decrypted_message={decrypted_message.decode("utf8")}')
        LOG.debug(f'CHAT: расшифрованное сообщение - {decrypted_message.decode("utf8")}')
        # Сохраняем сообщение в базу
        self.db_client.save_message(self.current_chat, 'in', decrypted_message.decode('utf8'))

        self.history_list_update()

    def history_list_update(self):
        pass
        # Получаем историю
        history_list = sorted(self.db_client.get_history(self.current_chat), key=lambda item: item[3])
        print(f'history_list= {history_list}')
        self.history_model = QStandardItemModel()
        self.ui_chat.list_messages.setModel(self.history_model)
        # Очистим от старых записей
        self.history_model.clear()
        # Берём не более 20 последних записей.
        length = len(history_list)
        start_index = 0
        if length > 20:
            start_index = length - 20
        # Заполнение модели записями, так-же стоит разделить входящие
        # и исходящие выравниванием и разным фоном.
        # отображает только последие 20 сообщений
        for i in range(start_index, length):
            item = history_list[i]
            if item[1] == 'in':
                if item[1] == 'in':
                    mess = QStandardItem(
                        f'Входящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                    mess.setEditable(False)
                    mess.setBackground(QBrush(QColor(255, 213, 213)))
                    mess.setTextAlignment(Qt.AlignLeft)
                    self.history_model.appendRow(mess)
                else:
                    mess = QStandardItem(
                        f'Исходящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                    mess.setEditable(False)
                    mess.setTextAlignment(Qt.AlignRight)
                    mess.setBackground(QBrush(QColor(204, 255, 204)))
                    self.history_model.appendRow(mess)
            self.ui_chat.list_messages.scrollToBottom()
