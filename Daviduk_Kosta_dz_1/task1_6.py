# 6. Создать текстовый файл test_file.txt,
# заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.


import glob
from chardet.universaldetector import UniversalDetector

txt = ['сетевое программирование\n', 'сокет\n', 'декоратор\n']

with open('test_file.txt', 'w', encoding='HZ-GB-2312') as f:
    f.writelines(txt)

# создаем детектор
# https://docs-python.ru/packages/modul-chardet-python-opredelenie-kodirovki/
detector = UniversalDetector()
for filename in glob.glob('*.txt'):
    print(filename.ljust(60), end='')
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
    enc = detector.result.get('encoding')

with open('test_file.txt', 'r', encoding=enc) as f:
    for line in f:
        print(line, end='')

# test_file.txt
# сетевое программирование
# сокет
# декоратор
