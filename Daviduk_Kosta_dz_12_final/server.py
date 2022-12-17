import sys
import argparse
import logging
from server_oop import Server
from server_d_b import ServerBase

import log.server_log_config

# python3 server.py
# python3 server.py -p 10000 -a 127.0.0.8

LOG = logging.getLogger('server')


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=7777)
    parser.add_argument('-a', '--addr', default='127.0.0.1')
    return parser


def main():
    LOG.debug('"Старт сервера"')
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    port = namespace.port
    address = namespace.addr

    db = ServerBase()

    server = Server(address, port, db)
    server.start()


if __name__ == '__main__':
    main()
