# -*- coding: utf-8 -*-
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop
# from tornado.web import Application, RequestHandler
# from tornado.netutil import bind_sockets

class Server1(TCPServer):

    listeners_streams = []

    async def handle_stream(self, stream, address):

        if stream.fileno().getsockname()[1] == 8888:
            # TODO: учёт множества источников
            try:
                while True:
                    try:
                        data_from_client = await stream.read_until(b'\r\n')
                        print('rec_data: {}'.format(data_from_client))
                        # await stream.write(data_from_client)
                    except StreamClosedError:
                        print('Client message StreamClosedError')
                        # TODO: сформулировать ответ источнику в случае неудачной обработки сообщения
                    except Exception as e:
                        print(str(e))
                        # TODO: сформулировать ответ источнику в случае совсем неудачной обработки сообщения
                        break
                    else:
                        # TODO: сформулировать ответ источнику в случае удачной обработки сообщения
                        if self.listeners_streams:
                            print('sending to listener: {}'.format(data_from_client))
                            # data_from_client ="from client! \r\n"
                            # TODO: for для каждого слушателя
                            await self.listeners_streams[0].write(data_from_client) #.encode('utf-8'))
                    finally:
                        # TODO: послать ответ источнику
                        pass
            except StreamClosedError:
                print('Client out')

        elif stream.fileno().getsockname()[1] == 8889:
            try:
                # while True:
                    sended_data = 'from server\r\n'
                    self.listeners_streams.append(stream)
                    print('sended_data: {}'.format(sended_data))
                    await stream.write(sended_data.encode('utf-8'))
            except StreamClosedError:
                print('Listener out')

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