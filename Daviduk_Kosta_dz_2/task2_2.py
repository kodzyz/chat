# 2. Есть файл orders в формате JSON с информацией о заказах.
# Написать скрипт, автоматизирующий его заполнение данными.
# Создать функцию write_order_to_json(),
# в которую передается 5 параметров —
# товар (item),
# количество (quantity),
# цена (price),
# покупатель (buyer),
# дата (date).
# Функция должна предусматривать
# запись данных в виде словаря в файл orders.json.
# {"orders": []}
# При записи данных указать величину отступа в 4 пробельных символа;
import json


def write_order_to_json(item, quantity, price, buyer, date):
    data = {}
    data['orders'] = []
    data['orders'].append({
        'item': f'{item}',
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    })

    with open('orders.json', 'a') as f:
        json.dump(data, f, indent=4)


write_order_to_json('Xiaomi Redmi 9C', 1, 11000, 'user1', '18.10.2022')
write_order_to_json('Xiaomi Redmi 9A', 1, 11000, 'user2', '17.12.2022')
