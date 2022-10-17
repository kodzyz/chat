# 4. Преобразовать слова
# «разработка», «администрирование», «protocol», «standard»
# из строкового представления в байтовое
# и выполнить обратное преобразование
# (используя методы encode и decode).


def enc(string):
    string_bytes = string.encode('utf-8')
    return string_bytes


def dec(bytes):
    bytes_string = bytes.decode('utf-8')
    return f'{type(bytes_string)}, {bytes_string}'


string_1 = (enc('разработка'))
string_2 = (enc('администрирование'))
string_3 = (enc('protocol'))
string_4 = (enc('standard'))

print(dec(string_1))
print(dec(string_2))
print(dec(string_3))
print(dec(string_4))

# <class 'str'>, разработка
# <class 'str'>, администрирование
# <class 'str'>, protocol
# <class 'str'>, standard
