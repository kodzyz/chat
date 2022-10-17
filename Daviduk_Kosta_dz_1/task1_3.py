# 3. Определить, какие из слов
# «attribute», «класс», «функция», «type»
# невозможно записать в байтовом типе.


def enc(string):
    string_bytes = bytes(string, 'utf-8')
    return f'{string_bytes}, '


print(enc('attribute'))
print(enc('класс'))  # невозможно записать в байтовом типе
print(enc('функция'))  # невозможно записать в байтовом типе
print(enc('type'))

# b'attribute',
# b'\xd0\xba\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81',
# b'\xd1\x84\xd1\x83\xd0\xbd\xd0\xba\xd1\x86\xd0\xb8\xd1\x8f',
# b'type',
