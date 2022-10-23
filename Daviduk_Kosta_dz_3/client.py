from socket import *
import json
import time
import sys
import argparse


# python3 server.py 10000 127.0.0.8

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default='127.0.0.1')
    parser.add_argument('port', type=int, default=7777)
    return parser


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((address, port))

    msg = {
        "action": "presence",
        "time": int(time.time()),
        "type": "status",
        "user": {
            "account_name": "dacope",
            "status": "Yep, I am here!"
        }
    }
    js_msg = json.dumps(msg)
    s.send(js_msg.encode('utf-8'))

    data = s.recv(1024)
    dec_data = data.decode('utf-8')
    js_data = json.loads(dec_data)
    print(js_data)


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    port = namespace.port
    address = namespace.addr
    # print(port, address)
    main()

# python3 client.py 127.0.0.1 7777
# {'response': 200, 'alert': 'OK'}

# python3 client.py 127.0.0.8 10000
# {'response': 200, 'alert': 'OK'}
