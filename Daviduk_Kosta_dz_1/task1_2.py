# 2. Каждое из слов
# «class», «function», «method»
# записать в байтовом типе без преобразования в последовательность кодов
# (не используя методы encode и decode)
# и определить тип, содержимое и длину соответствующих переменных.


def enc(string):
    string_bytes = bytes(string, 'utf-8')
    return f'{type(string_bytes)}, {string_bytes}, {len(string_bytes)}'


print(enc('class'))
print(enc('function'))
print(enc('method'))

# <class 'bytes'>, b'class', 5
# <class 'bytes'>, b'function', 8
# <class 'bytes'>, b'method', 6
