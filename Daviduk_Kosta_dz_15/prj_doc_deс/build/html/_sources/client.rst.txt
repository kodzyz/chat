Client module
=================================================

Клиентское приложение для обмена сообщениями. Поддерживает
отправку сообщений пользователям которые находятся в сети.

Поддерживает аргументы коммандной строки:

``python client.py {имя сервера} {порт}``

1. {имя сервера} - адрес сервера сообщений.
2. {порт} - порт по которому принимаются подключения

Примеры использования:

* ``python client.py``

*Запуск приложения с параметрами по умолчанию.*

* ``python client.py ip_address some_port``

*Запуск приложения с указанием подключаться к серверу по адресу ip_address:port*

client.py
~~~~~~~~~

Запускаемый модуль,содержит функционал инициализации приложения.
Выполняет проверку на корректность номера порта.
Создаёт клиентокое приложение на основе PyQt5.

client. **createParser** ()
    Парсер аргументов командной строки, определяет 2 элемента:

    * адрес сервера
    * порт

client. **keys_message** ()
    Генерация ключей с длинной 2048 bit для шифрований сообщений с помощью алгоритма RSA.

client. **client_authenticate** (connection)
    Аутентификация клиента на удаленном сервисе.

    * Параметр connection - сетевое соединение (сокет)
    * secret_key - ключ шифрования, известный клиенту и серверу

client_d_b.py
~~~~~~~~~~~~~

.. autoclass:: client_d_b.ClientBase
    :members:
	
client_oop.py
~~~~~~~~~~~~~

.. autoclass:: client_oop.Recept
    :members:

client_oop.py
~~~~~~~~~~~~~

.. autoclass:: client_oop.Send
	:members:

main_window.py
~~~~~~~~~~~~~~

.. autoclass:: client.main_window.ClientMainWindow
    :members:

main_chat.py
~~~~~~~~~~~~~~

.. autoclass:: client.main_chat.MainChat
    :members:

start_dialog.py
~~~~~~~~~~~~~~~

.. autoclass:: client.start_dialog.UserNameDialog
	:members:


add_contact.py
~~~~~~~~~~~~~~

.. autoclass:: client.add_contact.AddContactDialog
	:members:
	
	
del_contact.py
~~~~~~~~~~~~~~

.. autoclass:: client.del_contact.DelContactDialog
	:members: