# -*- coding: utf-8 -*-
"""
Created on Tue May 24 14:18:09 2022

@author: DTEAIAPPS
"""

import zmq

context = zmq.Context()

print("COnnecting to the server...")

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

for request in range(1000000):
    
    # print(f"Sending request # :{request}")
    socket.send_string("Hello")
    
    message = socket.recv()
    
    if request % 100000 == 1:
        print(f"Recieved reply for request: {request} is [{message}]")