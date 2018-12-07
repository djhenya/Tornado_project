from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop
# from tornado.web import Application, RequestHandler
# from tornado.netutil import bind_sockets

# class MainHandler(RequestHandler):
#     def get(self):
#         self.write("Hello, world")


class Server1(TCPServer):
    async def handle_stream(self, stream, address):
        while True:
            try:
                data = await stream.read_until(b'\n')
                print(data)
                # await stream.write(data)
            except StreamClosedError:
                break

# class Server2(TCPServer):
#     async def handle_stream(self, stream, address):
#         print('ok')
#         await stream.write(b'hello')


if __name__ == '__main__': 

    # app = Application([
    #     (r"/", Server1),
    #     # (r"/2", Server2)
    # ])
    # app.listen(8888)
    # app.listen(8889)

    server1 = Server1()
    server1.listen(8888)
    server1.listen(8889)

    # server2 = Server2()
    # server2.listen(8889)

    # server1.add_sockets(bind_sockets(8888))
    # server1.add_sockets(bind_sockets(8889))
    IOLoop.current().start()