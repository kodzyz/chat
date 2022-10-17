# 1. Каждое из слов
# «разработка», «сокет», «декоратор»
# представить в строковом формате и проверить тип и содержание соответствующих переменных.
# Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
# и также проверить тип и содержимое переменных.


string_1 = 'разработка'
print(type(string_1), string_1) # <class 'str'> разработка
string_1_unic = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
print(type(string_1_unic), string_1_unic) # <class 'str'> разработка

string_2 = 'сокет'
print(type(string_2), string_2) # <class 'str'> сокет 
string_2_unic = '\u0441\u043e\u043a\u0435\u0442'
print(type(string_2_unic), string_2_unic) # <class 'str'> сокет

string_3 = 'декоратор'
print(type(string_3), string_3) # <class 'str'> декоратор
string_3_unic = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
print(type(string_3_unic), string_3_unic) # <class 'str'> декоратор


