# Написать функцию host_range_ping_tab(),
# возможности которой основаны на функции из примера 2.
# Но в данном случае результат должен быть итоговым по всем ip-адресам,
# представленным в табличном формате (использовать модуль tabulate).
# Таблица должна состоять из двух колонок:

# pip install tabulate

from tabulate import tabulate
import json
from task9_2 import host_range_ping


def host_range_ping_tab():
    host_range_ping()
    with open('orders.json') as f:
        data = json.load(f)
        print(tabulate(data, headers='keys', tablefmt="pipe"))


if __name__ == '__main__':
    host_range_ping_tab()


# Узел 128.0.1.10 доступен
# Узел 128.0.1.11 недоступен
# Узел 128.0.1.12 недоступен
# | Reachable   | Unreachable   |
# |:------------|:--------------|
# | 128.0.1.10  | 128.0.1.11    |
# |             | 128.0.1.12    |
