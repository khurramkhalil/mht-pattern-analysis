# -*- coding: utf-8 -*-
"""
Created on Tue May 31 09:14:13 2022

@author: DTEAIAPPS
"""

import socket
import json


HOST, PORT = "localhost", 9999

raw_data = {"id": 2, "name": "abc"}
data = json.dumps(raw_data)
data = bytes(data, encoding="utf-8")

# Create a socket (SOCK_STREAM means a UDP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = (HOST, PORT)
sock.bind(server_address)

print("Server is running")

while True:
    print("Server is listening")
    recv_data = sock.recvfrom(4096)
    print(f"Client message: {recv_data[0]}")
    
    address = recv_data[1]
    
    print("Sending reply to the client")
    sock.sendto(data, address)
    

