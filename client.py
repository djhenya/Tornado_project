# -*- coding: utf-8 -*-
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient
# from tornado.options import options

from msg_creator import create_msg
from msg_parser import parse_msg

tcp_client = TCPClient()

async def client():
  # while True:
    try:
        stream = await tcp_client.connect('localhost', 8888)

        while True:
            # msg ="from client! \r\n"
            msg = create_msg('client')
            await stream.write(msg.encode('utf-8'))
            await gen.sleep(5)
            # TODO: обработать ответ от сервера
            # data = await stream.read_until(b'l')
            # print(data)
    except StreamClosedError:
        print("Server is unavailable.")
        # stream.close()
    # except KeyboardInterrupt:
    #     print("Client is killed.")
    #     stream.close()

# loop = IOLoop.current()
# loop.spawn_callback(client)
# loop.start()

if __name__ == '__main__':
    # options.parse_command_line()
    # client_id = input('Enter client id:').encode('utf-8')

    print("Client start.")
    IOLoop.current().run_sync(client)