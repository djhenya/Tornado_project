# -*- coding: utf-8 -*-

from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop
# from tornado.web import Application, RequestHandler
# from tornado.netutil import bind_sockets

from datetime import datetime
from struct import unpack, error
import logging

from msg_creator import create_msg

class Server(TCPServer):

    listeners_streams = []
    clients_streams = []

    async def handle_stream(self, stream, address):

        if stream.fileno().getsockname()[1] == 8888: # если подключение по порту 8888 (источник)
            logging.info('New client.')
            self.clients_streams.append(stream) # добавление tcp-сессии в список имеющихся сессий с источниками
            # try:
            while True:
                    try:
                        head_msg_from_client = await stream.read_bytes(13)
                        stream.last_msg_time = datetime.now() # запись момента приёма сообщения
                        header, msg_id, client_id, client_status, numfields = unpack("!Bh8sBB", head_msg_from_client)
                        msg_from_client = await stream.read_bytes(numfields * 12 + 1)
                        fields_packed, ctrl_sum = unpack('{}sB'.format(numfields * 12), msg_from_client)
                        
                        client_id = client_id.decode('utf-8').rstrip('\x00')
                        fields = self.unpack_fields(fields_packed, numfields)

                        msg_from_client_parsed = (header, msg_id, client_id, client_status, numfields, fields, ctrl_sum)
                        logging.info('Receiving from client: {}'.format(str(msg_from_client_parsed))) # Сообщение от источника
                    except StreamClosedError:
                        logging.warning('Client out')
                        self.clients_streams.remove(stream)
                        # данные для ответа источнику в случае неудачной обработки сообщения:
                        msg_id = 0
                        msg_to_client_header = 0x12
                        break
                    except error as se:
                        logging.error('Bad message from client: {}'.format(str(se)))
                        # данные для ответа источнику в случае неудачной обработки сообщения:
                        msg_id = 0
                        msg_to_client_header = 0x12
                    except Exception as e:
                        logging.critical(str(e))
                        self.clients_streams.remove(stream)
                        # данные для ответа источнику в случае неудачной обработки сообщения:
                        msg_id = 0
                        msg_to_client_header = 0x12
                        break
                    else:
                        stream.last_msg_id, stream.id, stream.status = msg_id, client_id, self.translate_status(client_status)
                        stream.fields = fields

                        # сформулировать header ответа источнику в случае удачной обработки сообщения
                        msg_to_client_header = 0x11

                        # Пересылка слушателю:
                        if self.listeners_streams:
                            msg_to_listener = ''
                            for k, v in fields.items():
                                msg_to_listener += '[' + str(stream.id) + '] ' + str(k) + ' | ' + str(v) + '\r\n'
                            logging.info('Sending to listeners from clients: {}'.format(msg_to_listener))
                            for listener_stream in self.listeners_streams:
                                try:
                                    await listener_stream.write(msg_to_listener.encode('utf-8'))
                                except StreamClosedError:
                                    logging.warning('Listener out')
                                    self.listeners_streams.remove(listener_stream)

                    # послать ответ источнику:
                    msg_to_client = create_msg('server', header=msg_to_client_header, last_msg_id=msg_id)
                    logging.info('Response to client: {}'.format(msg_to_client))
                    try:
                        await stream.write(msg_to_client)
                    except StreamClosedError:
                        logging.warning('Client out')
                        self.clients_streams.remove(stream)
            # except StreamClosedError:
            #     print(' out')
            # except KeyboardInterrupt:
            #     stream.close()

        elif stream.fileno().getsockname()[1] == 8889: # если подключение по порту 8889 (слушатель)
            try:
                logging.info('New listener.')
                self.listeners_streams.append(stream)
                # сообщение при подключении слушателя - список всех источников (в определённом формате)
                welcome_msg = ''
                if self.clients_streams:
                    for client in self.clients_streams:
                        dt = datetime.now() - client.last_msg_time
                        time_from_last_msg = str(round((dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0))
                        # welcome_msg.join('[{}] {} | {} {}\r\n'.format( str(client.id), str(client.last_msg_id), str(client.status), time_from_last_msg ))
                        welcome_msg += '[' + str(client.id) + '] ' + str(client.last_msg_id) + ' | ' + str(client.status) + ' | ' + time_from_last_msg + '\r\n'
                else:
                    welcome_msg = 'There is no clients yet.\r\n'
                logging.info('Welcome message to listener: {}'.format(welcome_msg))
                await stream.write(welcome_msg.encode('utf-8'))
            except StreamClosedError:
                logging.warning('Listener out')
                self.listeners_streams.remove(listener_stream)

    @staticmethod
    def translate_status(status_value):
        if status_value == 0x01: return 'IDLE'
        if status_value == 0x02: return 'ACTIVE'
        if status_value == 0x03: return 'RECHARGE'

    @staticmethod
    def unpack_fields(fields_struct, fields_count):
        fields_tuple = unpack('!' + '8sI' * fields_count, fields_struct)
        fiels_dict = {}
        for item in fields_tuple:
            if isinstance(item, bytes):
                field_name = item.decode('utf-8').rstrip('\x00')
            else:
                fiels_dict.update({field_name: item})
        return fiels_dict


if __name__ == '__main__': 

    # app = Application([
    #     (r"/", Server1),
    #     # (r"/2", Server2)
    # ])
    # app.listen(8888)
    # app.listen(8889)

    LOG_FORMAT = '%(levelname)s, %(asctime)s - %(message)s'
    logging.basicConfig(filename = 'server.log', filemode='w', format=LOG_FORMAT, level=logging.INFO)
    logger = logging.getLogger()

    logging.info("Server start.")
    server = Server()
    server.listen(8888)
    server.listen(8889)

    # server.add_sockets(bind_sockets(8888))
    # server.add_sockets(bind_sockets(8889))
    IOLoop.current().start()