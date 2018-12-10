# -*- coding: utf-8 -*-
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient
# from tornado.options import options

import logging

tcp_client = TCPClient()

async def listen():
    try:
        stream = await tcp_client.connect('localhost', 8889)

        while True:
            response = await stream.read_until(b"\r\n")
            response = response.decode('utf-8').rstrip('\r\n')
            logging.info(response)
    except StreamClosedError:
        logging.info("Server is unavailable. Listener is shutted down.")
    # except KeyboardInterrupt:
    #     print("Listener is killed.")
    #     stream.close()


if __name__ == '__main__':
    # options.parse_command_line()

    LOG_FORMAT = '%(message)s'
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)

    logging.info("Listener start.")
    IOLoop.current().run_sync(listen)