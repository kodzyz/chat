from socket import *
import json
import sys
import argparse


# python3 server.py -p 10000 -a 127.0.0.8

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=7777)
    parser.add_argument('-a', '--addr', default='127.0.0.1')
    return parser


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((address, port))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Получаем запрос на соединение:', addr)

        data = conn.recv(1024)
        dec_data = data.decode('utf-8')
        js_data = json.loads(dec_data)
        print(js_data)
        if js_data['action'] == 'presence':
            reply = {
                'response': 200,
                'alert': 'OK'
            }
            js_reply = json.dumps(reply)
            conn.send(js_reply.encode('utf-8'))
        else:
            reply = {
                'response': 400,
                'alert': 'Bad Request'
            }
            js_reply = json.dumps(reply)
            conn.send(js_reply.encode('utf-8'))


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    port = namespace.port
    address = namespace.addr
    main()

# python3 server.py
# Получаем запрос на соединение: ('127.0.0.1', 41540)
# {'action': 'presence', 'time': 1666527102, 'type': 'status', 'user': {'account_name': 'dacope', 'status': 'Yep, I am here!'}}

# python3 server.py -p 10000 -a 127.0.0.8
# Получаем запрос на соединение: ('127.0.0.1', 48882)
# {'action': 'presence', 'time': 1666527164, 'type': 'status', 'user': {'account_name': 'dacope', 'status': 'Yep, I am here!'}}
