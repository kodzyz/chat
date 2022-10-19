# 3. Написать скрипт, автоматизирующий сохранение данных
# в файле YAML-формата.
# Подготовить данные для записи в виде словаря, в котором
# первому ключу соответствует список,
# второму — целое число,
# третьему — вложенный словарь,
# где значение каждого ключа — это целое число с юникод-символом,
# отсутствующим в кодировке ASCII (например, €);
# Реализовать сохранение данных в файл формата YAML —
# например, в файл file.yaml.
# При этом обеспечить стилизацию файла
# с помощью параметра default_flow_style,
# а также установить возможность работы с юникодом:
# allow_unicode = True;
# Реализовать считывание данных из созданного файла и проверить,
# совпадают ли они с исходными.

import yaml


def write_order_to_yaml(list_, int_, dict_):
    data = {
        '💪': list_,
        '🙌': int_,
        '👏': dict_
    }

    with open('data.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=True, allow_unicode=True)


to_list = ['list1', 'list2', 'list3']
to_int = 5
to_dict = {}
to_dict['dict1'] = {'action': 'msg', 'to': 'account_name', 'from': 'account_name'}

write_order_to_yaml(to_list, to_int, to_dict)

with open('data.yaml') as f:
    content = yaml.safe_load(f)
print(content)
yam_data = yaml.dump(content, allow_unicode=True)
print(yam_data)

# {'👏': {'dict1': {'action': 'msg', 'from': 'account_name', 'to': 'account_name'}}, '💪': ['list1', 'list2', 'list3'], '🙌': 5}
# 👏:
#   dict1:
#     action: msg
#     from: account_name
#     to: account_name
# 💪:
# - list1
# - list2
# - list3
# 🙌: 5

