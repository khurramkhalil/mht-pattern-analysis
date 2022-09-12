# -*- coding: utf-8 -*-
"""
Created on Tue May 31 09:27:18 2022

@author: DTEAIAPPS
"""

import json
import socket
# import time

HOST, PORT = "localhost", 9999

data = str.encode("Hello from the UDP client")

# Creating UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Binding Port
server_address = (HOST, PORT)
# sock.bind(server_address)

count = 1
while count < 10000:
    # time.sleep(0.01)
    # Request to the server
    sock.sendto(data, server_address)
    
    # Recieving from the server
    rec_data = sock.recvfrom(4096)
    json_obj = json.loads(rec_data[0])
    # print(json_obj)
    
    count += 1


