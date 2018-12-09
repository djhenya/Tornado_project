# -*- coding: utf-8 -*-

def parse_msg(message, source):
    if source == 'client': return message
    if source == 'server': return message