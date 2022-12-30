import logging

log = logging.getLogger('server')

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s - %(message)s ")

file_handler = logging.FileHandler('app_server.log', encoding='utf-8')
file_handler.setFormatter(formatter)

log.addHandler(file_handler)
log.setLevel(logging.DEBUG)


if __name__ == '__main__':
    log.info('Информационное сообщение')

