# -*- coding: utf-8 -*-
from struct import pack

def create_msg(source):

    if source == 'client':
        client_message_format = {
            'header': 0x01,
            'msg_id': 0,
            'client_id': b'abcd',
            'status': 0x01,
            'numfields': 6,
            'fields': [
                (b'first', 21),
                (b'second', 100),
                (b'third', 74),
                (b'fourth', 123),
                (b'unite', 41),
                (b'temp', 22),
            ]
        }

        fields = [
                (b'Message', 1),
                (b'from', 2),
                (b'client', 3),
            ]
        fields_string = b''.join([pack('!8sI', k, v) for k, v in fields])
        message_list_hardcode = [
            0x01,
            0,
            b'abcd',
            0x01,
            6,
            fields_string
        ]
        client_message = pack('!Bh8sBB3060p', *message_list_hardcode)
        client_message += xor(client_message) # TODO: доделать
        return client_message

    if source == 'server':
        server_message_format = {}
        return server_message_format