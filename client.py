# -*- coding: utf-8 -*-
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient

tcp_client = TCPClient()

async def client():
  # while True:
    try:
        stream = await tcp_client.connect('localhost', 8888)

        while True:
            msg ="from client! \r\n"
            await stream.write(msg.encode('utf-8'))
            await gen.sleep(5)
            # TODO: обработать ответ от сервера
            # data = await stream.read_until(b'l')
            # print(data)

    except StreamClosedError:
        print("error connecting")
        stream.close()

loop = IOLoop.current()
loop.spawn_callback(client)
loop.start()

# if __name__ == '__main__':
#     options.parse_command_line()
#     IOLoop.instance().run_sync(client)