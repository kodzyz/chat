import time

from Cryptodome.Cipher import PKCS1_OAEP
from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox, QApplication, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSlot, QEvent, Qt
import sys
import json
import logging
from server_d_b import ServerBase
from client.list_client_window import Ui_MainClientWindow
from client.main_chat import MainChat
from client.add_contact import AddContactDialog
from client.del_contact import DelContactDialog

LOG = logging.getLogger('client')


class ClientMainWindow(QMainWindow):
    '''
    Класс - основное окно пользователя.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированого файла list_client_window.py
    '''
    def __init__(self, database_client, recept_transport, send_transport, login, keys):
        super().__init__()
        # основные переменные
        self.db_client = database_client
        self.recept = recept_transport
        self.send = send_transport
        self.login = login


        # Загружаем конфигурацию окна из дизайнера
        self.ui_list = Ui_MainClientWindow()
        self.ui_list.setupUi(self)

        # Кнопка "Выход"
        self.ui_list.menu_exit.triggered.connect(qApp.exit)

        # "добавить контакт"
        self.ui_list.btn_add_contact.clicked.connect(self.add_contact_window)

        # "Удалить контакт"
        self.ui_list.btn_remove_contact.clicked.connect(self.delete_contact_window)

        # лист контактов
        self.clients_list_update()

        # Даблклик по листу контактов отправляется в обработчик
        self.ui_list.list_contacts.doubleClicked.connect(self.select_active_user)

        # Дополнительные требующиеся атрибуты
        self.contacts_model = None
        self.current_chat = None

        self.show()

        self.chat = MainChat(self.db_client, self.send, self.recept, keys)

        # Обработчик сигнала, связанного с объектом
        self.recept.new_message.connect(self.chat.message_signal)

    def add_contact_window(self):
        '''Метод создающий окно - диалог добавления контакта'''
        add_dialog = AddContactDialog()
        add_dialog.btn_ok.clicked.connect(lambda: self.add_contact_action(add_dialog))
        add_dialog.show()

    def add_contact_action(self, item):
        '''Метод обработчик нажатия кнопки "Добавить"'''
        new_contact = item.client_name.text()
        self.add_contact(new_contact)
        # print(new_contact)
        item.close()

    def add_contact(self, add_contact):
        '''
        Метод добавляющий контакт в серверную BD.
        '''
        self.send.add_contact(add_contact)
        time.sleep(1)
        self.clients_list_update()

    def delete_contact_window(self):
        '''Метод создающий окно удаления контакта.'''
        remove_dialog = DelContactDialog()
        remove_dialog.btn_ok.clicked.connect(lambda: self.remove_contact_action(remove_dialog))
        remove_dialog.show()

    def remove_contact_action(self, item):
        remove_contact = item.client_name.text()
        self.remove_contact(remove_contact)
        # print(remove_contact)
        item.close()

    def remove_contact(self, remove_contact):
        '''
        Метод удаляющий контакт из серверной BD.
        '''
        self.send.del_contact(remove_contact)
        time.sleep(1)
        self.clients_list_update()

    def clients_list_update(self):
        '''Метод обновляющий список контактов.'''
        self.send.contacts()
        time.sleep(1)
        contacts_list = self.recept.contact_list
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui_list.list_contacts.setModel(self.contacts_model)
        # print(contacts_list)

    # Функция обработчик даблклика по контакту
    def select_active_user(self):
        '''Метод обработчик события двойного клика по списку контактов.'''
        # Выбранный пользователем (даблклик) находится в выделеном элементе в QListView
        self.current_chat = self.ui_list.list_contacts.currentIndex().data()
        # print(f'даблклик - {self.current_chat}')

        # вызываем основную функцию
        self.set_active_user()

    # Функция устанавливающяя активного собеседника
    def set_active_user(self):
        '''Метод активации чата с собеседником.'''
        # print('даблклик')
        self.chat.setWindowTitle(f'Чат "{self.login}"')
        self.chat.show()
        self.chat.current_receive(self.current_chat)
