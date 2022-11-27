# Продолжаем работать над проектом «Мессенджер»:
# a. Реализовать скрипт, запускающий два клиентских приложения: на чтение чата и на
# запись в него. Уместно использовать модуль subprocess);
# b. Реализовать скрипт, запускающий указанное количество клиентских приложений.

from subprocess import Popen, CREATE_NEW_CONSOLE

p_list = []
# Список клиентских процессов
while True:
    user = input("Запустить N клиентов:  / Закрыть клиентов (x) / Выйти (q) ")
    if user == 'q':
        break
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
    else:
        for _ in range(int(user)):
            # Флаг CREATE_NEW_CONSOLE нужен для ОС Windows,
            # чтобы каждый процесс запускался в отдельном окне консоли
            p_list.append(Popen('python3 client.py',
                                creationflags=CREATE_NEW_CONSOLE))
        print(f'Запущено {user} клиентов')

