from socket import *
import json
import sys
import argparse
from my_func import js_dec, js_enc


# python3 server.py
# python3 server.py -p 10000 -a 127.0.0.8

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=7777)
    parser.add_argument('-a', '--addr', default='127.0.0.1')
    return parser


def pars_listen(data):
    if data['action'] == 'presence':
        return {
            'response': 200,
            'alert': 'OK'
        }
    return {
        'response': 400,
        'alert': 'Bad Request'
    }


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((address, port))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Получаем запрос на соединение:', addr)
        listen = js_dec(conn.recv(1024))
        print(listen)
        reply = pars_listen(listen)
        conn.send(js_enc(reply))


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    port = namespace.port
    address = namespace.addr
    main()
