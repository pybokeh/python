# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 15:59:13 2012

@author: pybokeh
"""

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.1'
port = 1060
max_data = 65535
message = 'Hello server, this is client!'
s.sendto(message, (host, port))
data, address = s.recvfrom(max_data)
server_ip, server_port = address
print 'The server with ip', server_ip, 'and port', server_port, 'says', repr(data)
print 's.getsockname():', s.getsockname()