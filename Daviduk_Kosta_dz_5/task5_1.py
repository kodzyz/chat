# 1. В директории проекта создать каталог log,
# в котором для клиентской и серверной сторон в отдельных модулях
# формата client_log_config.py и server_log_config.py
# создать логгеры;

# 2. В каждом модуле выполнить настройку соответствующего логгера
# по следующему алгоритму:
# Создание именованного логгера;
# Сообщения лога должны иметь следующий формат:
# "<дата-время> <уровень важности> <имямодуля> <сообщение>";
# Журналирование должно производиться в лог-файл;
# На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.

# 3. Реализовать применение созданных логгеров для решения двух задач:
# Журналирование обработки исключений try/except.
# Вместо функции print() использовать журналирование и
# обеспечить вывод служебных сообщений в лог-файл;
# Журналирование функций, исполняемых на серверной и клиентской сторонах
# при работе мессенджера.
