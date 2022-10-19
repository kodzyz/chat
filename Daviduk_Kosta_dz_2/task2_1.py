# Написать скрипт, осуществляющий выборку определенных данных из файлов
# info_1.txt, info_2.txt, info_3.txt
# и формирующий новый «отчетный» файл в формате CSV.

import glob
import re
import csv

from chardet.universaldetector import UniversalDetector

detector = UniversalDetector()
for filename in glob.glob('*.txt'):
    # print(filename.ljust(60), end='')
    # сбрасываем детектор
    # в исходное состояние
    detector.reset()
    # проходимся по строкам очередного
    # файла в режиме 'rb'
    for line in open(filename, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()
    # print(detector.result)
# info_3.txt    {'encoding': 'windows-1251', 'confidence': 0.9410155329825751, 'language': 'Russian'}
# info_2.txt    {'encoding': 'windows-1251', 'confidence': 0.9416013526034656, 'language': 'Russian'}
# info_1.txt    {'encoding': 'windows-1251', 'confidence': 0.9417798857160135, 'language': 'Russian'}

os_prod_list = []
os_name_list = []
os_code_list = []
os_type_list = []
main_data = []

RE_PROD_PARS = re.compile(r"(Изготовитель системы):\s+(\w+)")
RE_NAME_PARS = re.compile(r'(Название ОС):\s+(\w+\s\w+\s\d\s\w+)')
RE_CODE_PARS = re.compile(r'(Код продукта):\s+(\d+-\w+-\d+-\d+)')
RE_TYPE_PARS = re.compile(r'(Тип системы):\s+(\w\d+-\w+\s\w+)')


def get_data():
    file_name = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    for file in file_name:

        with open(file, 'r', encoding='windows-1251') as f:
            for l in f:
                if RE_PROD_PARS.match(l):
                    prod_pars = re.match(RE_PROD_PARS, l).groups()
                if RE_NAME_PARS.match(l):
                    name_pars = re.match(RE_NAME_PARS, l).groups()
                if RE_CODE_PARS.match(l):
                    code_pars = re.match(RE_CODE_PARS, l).groups()
                if RE_TYPE_PARS.match(l):
                    type_pars = re.match(RE_TYPE_PARS, l).groups()

            os_prod_list.append(prod_pars[1])
            os_name_list.append(name_pars[1])
            os_code_list.append(code_pars[1])
            os_type_list.append(type_pars[1])

    main_data.append(prod_pars[0])
    main_data.append(name_pars[0])
    main_data.append(code_pars[0])
    main_data.append(type_pars[0])

    return main_data, list(zip(os_prod_list, os_name_list, os_code_list, os_type_list))


def write_to_csv():
    head_list, data_list = get_data()

    with open('new_main_data.csv', 'w') as f:
        f_writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        f_writer.writerow(head_list)
        for row in data_list:
            f_writer.writerow(row)


write_to_csv()

with open('new_main_data.csv') as f:
    f_reader = csv.reader(f)
    for l in f_reader:
        print(l)

# ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
# ['LENOVO', 'Microsoft Windows 7 Профессиональная', '00971-OEM-1982661-00231', 'x64-based PC']
# ['ACER', 'Microsoft Windows 7 Профессиональная', '00971-OEM-1982661-00231', 'x64-based PC']
# ['DELL', 'Microsoft Windows 7 Профессиональная', '00971-OEM-1982661-00231', 'x86-based PC']
