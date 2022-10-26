from socket import *
import json
import time
import sys
import argparse
from my_func import js_dec, js_enc


# python3 client.py
# python3 client.py 127.0.0.8 10000

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', nargs='?', default='127.0.0.1')
    parser.add_argument('port', nargs='?', type=int, default=7777)
    return parser


def pars_listen(data):
    if data['response'] == 200:
        return 'response: 200'
    return 'response: 400'


def online():
    return {
        "action": "presence",
        "time": int(time.time()),
        "type": "status",
        "user": {
            "account_name": "dacope",
            "status": "Yep, I am here!"
        }
    }


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((address, port))

    msg = online()
    s.send(js_enc(msg))
    listen = js_dec(s.recv(1024))
    print(pars_listen(listen))


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    port = namespace.port
    address = namespace.addr
    main()
