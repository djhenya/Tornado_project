# -*- coding: utf-8 -*-

from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop
# from tornado.web import Application, RequestHandler
# from tornado.netutil import bind_sockets

from datetime import datetime

from msg_parser import parse


class Server(TCPServer):

    listeners_streams = []
    clients_streams = []

    async def handle_stream(self, stream, address):

        if stream.fileno().getsockname()[1] == 8888:
            # TODO: учёт множества источников
            print('New client.')
            self.clients_streams.append(stream) # добавление tcp-сессии в список имеющихся сессий с источниками
            # try:
                while True:
                    try:
                        msg_from_client = await stream.read_until(b'\r\n')
                        print('rec_data: {}'.format(msg_from_client))
                        parsed_msg = parse_msg(msg_from_client, 'client')
                    except StreamClosedError:
                        print('Client out')
                    except Exception as e:
                        print(str(e))
                        # TODO: сформулировать ответ источнику в случае неудачной обработки сообщения
                    else:
                        stream.last_msg_id, stream.id = parsed_msg[1], parsed_msg[2]
                        stream.field, stream.status = parsed_msg[5], translate_status(parsed_msg[3])
                        stream.last_msg_time = datetime.now()
                        # TODO: сформулировать ответ источнику в случае удачной обработки сообщения
                        if self.listeners_streams:
                            print('sending to listeners: {}'.format(msg_from_client))
                            # msg_from_client ="from client! \r\n"
                            for listener_stream in self.listeners_streams:
                                try:
                                    await listener_stream.write(msg_from_client) #.encode('utf-8'))
                                except StreamClosedError:
                                    print('Listener out')
                                    self.listeners_streams.remove(listener_stream)

                    finally:
                        # TODO: послать ответ источнику
                        pass
            # except StreamClosedError:
            #     print(' out')
            # except KeyboardInterrupt:
            #     stream.close()

        elif stream.fileno().getsockname()[1] == 8889:
            try:
                # while True:
                print('New listener.')
                self.listeners_streams.append(stream)
                # TODO: сообщение при подключении слушателя - список всех источников (в определённом формате)
                # welcome_msg = 'Hello, listener!\r\n'
                welcome_msg = ''
                if self.clients_streams:
                    for client in self.clients_streams:
                        # if 'id' not in client.__dict__:
                        #     welcome_msg = 'There is no messages from client yet.\r\n'
                        # else:
                            dt = datetime.now() - client.last_msg_time
                            time_from_last_msg = str(round((dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0))
                            welcome_msg.join('[{}] {} | {} {}\r\n'.format( str(client.id), str(client.last_msg_id), str(client.status), time_from_last_msg ))
                    print(welcome_msg)
                else:
                    welcome_msg = 'There is no clients yet.\r\n'
                # print('welcome_msg: {}'.format(welcome_msg))
                await stream.write(welcome_msg.encode('utf-8'))
            except StreamClosedError:
                print('Listener out')
                self.listeners_streams.remove(listener_stream)

    @staticmethod
    def translate_status(status_value):
        if status_value == 0x01: return 'IDLE'
        if status_value == 0x02: return 'ACTIVE'
        if status_value == 0x03: return 'RECHARGE'


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

    print("Server start.")
    server = Server()
    server.listen(8888)
    server.listen(8889)

    # server.add_sockets(bind_sockets(8888))
    # server.add_sockets(bind_sockets(8889))
    IOLoop.current().start()