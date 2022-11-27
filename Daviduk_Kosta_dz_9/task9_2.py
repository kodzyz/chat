# Написать функцию host_range_ping() для перебора ip-адресов
# из заданного диапазона.
# Меняться должен только последний октет каждого адреса.
# По результатам проверки должно
# выводиться соответствующее сообщение.

import ipaddress
from task9_1 import host_ping
import socket


def host_range_ping(ip='128.0.1.10', row=3):
    """ : ip :ip-адрес
        : row : диапазон
    """
    host = []
    ip_addr = ipaddress.ip_address(ip)
    s = int(ip.split('.')[3])
    if 0 < s < 254:
        for i in range(row):
            host.append(str(ip_addr + i))
    else:
        return f'each of the numbers between the periods in an IP address are 0-255'
    return host_ping(host)


if __name__ == '__main__':
    sock = socket.gethostbyname(socket.gethostname())  # локальный ip
    host_range_ping(sock, 5)

# Узел 127.0.1.1 доступен
# Узел 127.0.1.2 доступен
# Узел 127.0.1.3 доступен
# Узел 127.0.1.4 доступен
# Узел 127.0.1.5 доступен
