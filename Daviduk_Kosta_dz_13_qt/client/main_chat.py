import time

from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox, QApplication, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSlot, QEvent, Qt
import sys
import json
import logging
from client.chat_window import Ui_MainClientWindow


class MainChat(QMainWindow):
    def __init__(self, send_transport):
        super().__init__()
        # основные переменные
        # self.db_client = database_client
        # self.recept = recept_transport
        self.send = send_transport

        # Загружаем конфигурацию окна из дизайнера
        self.ui_chat = Ui_MainClientWindow()
        self.ui_chat.setupUi(self)

        # Кнопка отправить сообщение
        self.ui_chat.btn_send.clicked.connect(self.send_message)

        # Дополнительные требующиеся атрибуты
        self.history_model = None
        self.current_chat = None

    # Функция устанавливающяя активного собеседника
    def current_receive(self, receive):
        self.current_chat = receive
        self.ui_chat.label_new_message.setText(f'Введите сообщенние для {self.current_chat}:')
        # Заполняем окно историю сообщений по требуемому пользователю
        self.history_list_update()

    # Функция отправки собщения пользователю
    def send_message(self):
        # Текст в поле, проверяем что поле не пустое затем забирается сообщение и поле очищается
        message_text = self.ui_chat.text_message.toPlainText()
        self.ui_chat.text_message.clear()
        if not message_text:
            return
        self.send.send_message(message_text, self.current_chat)

    def history_list_update(self):
        # Получаем историю
        history_list = self.send.history_message(self.current_chat)

        self.history_model = QStandardItemModel()
        for i in history_list:
            item = QStandardItem(i)
            item.setEditable(False)
            self.history_model.appendRow(item)
        self.ui_chat.list_messages.setModel(self.history_model)
