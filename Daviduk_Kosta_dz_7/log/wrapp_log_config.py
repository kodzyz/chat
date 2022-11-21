import logging

log_wrapp_server = logging.getLogger('wrapp_server')
log_wrapp_client = logging.getLogger('wrapp_client')

forma = logging.Formatter('%(asctime)-10s %(message)s')

handler_file_server = logging.FileHandler('wrapper_server.log', encoding='utf-8')
handler_file_client = logging.FileHandler('wrapper_client.log', encoding='utf-8')

handler_file_server.setFormatter(forma)
handler_file_client.setFormatter(forma)

log_wrapp_server.addHandler(handler_file_server)
log_wrapp_client.addHandler(handler_file_client)

log_wrapp_server.setLevel(logging.DEBUG)
log_wrapp_client.setLevel(logging.DEBUG)

if __name__ == '__main__':
    log_wrapp_server.info('Информационное сообщение')
    log_wrapp_client.info('Информационное сообщение')
