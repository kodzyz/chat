import collections
import logging
import dis

LOG = logging.getLogger('client')


class ClientVerifier(type):
    def __init__(cls, clsname, bases, clsdict):
        methods = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        # print(methods)
        if 'accept' in methods or 'listen' in methods or 'socket' in methods:
            LOG.critical('В классе используются функций "accept", "listen", "socket"')
        super().__init__(clsname, bases, clsdict)


class ServerVerifier(type):
    def __init__(cls, clsname, bases, clsdict):
        methods = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        if 'connect' in methods:
            LOG.critical('Использование метода "connect" недопустимо')
        if not ('SOCK_STREAM' in methods and 'AF_INET' in methods):
            LOG.critical('Некорректная инициализация сокета.')
        super().__init__(clsname, bases, clsdict)
