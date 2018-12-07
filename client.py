from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient

tcp_client = TCPClient()

async def client():
    while True:
        try:
            stream = await tcp_client.connect('localhost', 8888)

            # # Set TCP_NODELAY / disable Nagle's Algorithm.
            # stream.set_nodelay(True)

            while True:
                msg ="hello \n"
                await stream.write(msg.encode())
                await gen.sleep(5)
                # data = await stream.read_until(b'l')
                # print(data)

        except StreamClosedError:
            print("error connecting")

loop = IOLoop.current()
loop.spawn_callback(client)
loop.start()