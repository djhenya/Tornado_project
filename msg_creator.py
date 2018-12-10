# -*- coding: utf-8 -*-
from struct import pack, calcsize
from functools import reduce
# import sys

def create_msg(source, **kwargs):

    if source == 'client': # подготовка сообщения от источника серверу

        # TODO: перенести fields в файл? или input?
        fields = {
                b'Message': 1,
                b'from': 2,
                b'client': 3,
            }
        fields_packed = b''.join([pack('!8sI', k, v) for k, v in fields.items()]) # подготовка пар полей данных

        # сообщение в формате списка:
        message_list = [
            0x01,
            kwargs['msg_id'],
            kwargs['source_id'],
            kwargs['source_status'],
            len(fields),
            fields_packed
        ] 
        pack_format = '!Bh8sBB{}s'.format(len(fields)*12) # формат упаковки сообщения
        # Про меня:
        # The form '!' is available for those poor souls who claim they can’t remember whether network byte order is big-endian or little-endian.
        # https://docs.python.org/3.7/library/struct.html#format-characters

    if source == 'server': # подготовка ответа от сервера источнику 

        message_list = [
            kwargs['header'],
            kwargs['last_msg_id'],
        ]        
        pack_format = '!Bh'

    message = pack(pack_format, *message_list) # упаковка сообщения
    # print(message, calcsize(pack_format))

    ctrl_sum = reduce((lambda x, y: x ^ y), message) # побайтовый XOR от сообщения
    # print(ctrl_sum)
    message += pack('B', ctrl_sum) # включение XOR в сообщение
    return message