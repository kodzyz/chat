# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com
# и преобразовать результаты из байтовового в строковый тип на кириллице.

import subprocess

args1 = ['ping', 'yandex.ru']
args2 = ['ping', 'youtube.com']

subproc_ping1 = subprocess.Popen(args1, stdout=subprocess.PIPE)

for line in subproc_ping1.stdout:
    l = line.decode('ascii').encode('utf-8')
    print(l.decode('utf-8'))

subproc_ping2 = subprocess.Popen(args2, stdout=subprocess.PIPE)

for line in subproc_ping2.stdout:
    l = line.decode('Windows-1254').encode('utf-8')
    print(l.decode('utf-8'))

# >>> import urllib.request, chardet
# >>> rawdata = urllib.request.urlopen('http://yandex.ru/').read()
# >>> chardet.detect(rawdata)
# {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}

# >>> import urllib.request, chardet
# >>> rawdata = urllib.request.urlopen('https://www.youtube.com/').read()
# >>> chardet.detect(rawdata)
# {'encoding': 'Windows-1254', 'confidence': 0.42843297122624036, 'language': 'Turkish'}
