# -*- coding: utf-8 -*-
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient
# from tornado.options import options

from struct import unpack
import logging

from msg_creator import create_msg

tcp_client = TCPClient()

async def client():
    try:
        client_id = input('Enter client id (max 8 chars): ').encode('utf-8')
        # client_id = b'asdffdsa'
        client_statuses = {'IDLE': 0x01, 'ACTIVE': 0x02, 'RECHARGE': 0x03}
        client_status = input('Enter client status (IDLE, ACTIVE or RECHARGE): ') #.encode('utf-8')
        # client_status = 'IDLE'
        if client_status not in client_statuses.keys():
            raise Exception('Wrong status!')
        else:
            client_status_value = client_statuses[client_status]
        stream = await tcp_client.connect('localhost', 8888)
        msg_number = 1

        while True:
            msg_to_server = create_msg('client', source_id=client_id, msg_id=msg_number, source_status=client_status_value)
            msg_number += 1
            
            logging.info('Message to server: {}'.format(msg_to_server))
            await stream.write(msg_to_server) # периодическая отправка сообщения на сервер
            await gen.sleep(5)
            
            msg_from_server = await stream.read_bytes(4) # приём ответа от сервера
            header, last_msg_id, ctrl_sum = unpack("!BhB", msg_from_server) # распаковка сообщения от сервера
            logging.info('Response from server: {}, {}, {}'.format(header, last_msg_id, ctrl_sum))

    except StreamClosedError:
        logging.info("Server is unavailable. Client is shutted down.")
    # except KeyboardInterrupt:
    #     print("Client is killed.")
    #     stream.close()

if __name__ == '__main__':
    # options.parse_command_line()

    LOG_FORMAT = '%(levelname)s, %(asctime)s - %(message)s'
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)

    logging.info("Client start.")
    IOLoop.current().run_sync(client)

    # loop = IOLoop.current()
    # loop.spawn_callback(client)
    # loop.start()