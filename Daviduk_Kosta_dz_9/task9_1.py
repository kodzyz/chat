# Написать функцию host_ping(),
# в которой с помощью утилиты ping будет проверяться
# доступность сетевых узлов.
# Аргументом функции является список,
# в котором каждый сетевой узел должен быть представлен именем хоста
# или ip-адресом.
# В функции необходимо перебирать ip-адреса и проверять их доступность
# с выводом соответствующего сообщения
# («Узел доступен», «Узел недоступен»).
# При этом ip-адрес сетевого узла должен создаваться с
# помощью функции ip_address().

import socket
import subprocess
import ipaddress
import json


def write_order_to_json(item1, item2):
    data = {}
    data['Reachable'] = item1
    data['Unreachable'] = item2

    with open('orders.json', 'w') as f:
        json.dump(data, f, indent=4)


def host_ping(host):
    """: -c1 :количество пакетов для отправки
    """
    host_reach = []
    host_unreach = []
    for i in host:
        try:
            addr = ipaddress.ip_address(i)
        except:
            pass
        addr = socket.gethostbyname(i)  # преобразует имя хоста/домена hostname в формат адреса IPv4
        command = ['ping', '-c', '1', addr]
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        p.wait()
        if p.poll() == 0:
            print(f'Узел {i} доступен')
            host_reach.append(i)

        else:
            print(f'Узел {i} недоступен')
            host_unreach.append(i)
        write_order_to_json(host_reach, host_unreach)


if __name__ == '__main__':
    args = ['ya.ru', 'google.com', 'yandex.ru', '87.250.250.242', '192.168.0.101']
    host_ping(args)

# Узел ya.ru доступен
# Узел google.com доступен
# Узел yandex.ru доступен
# Узел 87.250.250.242 доступен
# Узел 192.168.0.101 недоступен
