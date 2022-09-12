# -*- coding: utf-8 -*-
"""
Created on Tue May 24 14:14:41 2022

@author: DTEAIAPPS
"""

import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    # print(f"Recieved message: {message}")
    
    # time.sleep(1)
    
    socket.send_string("Worldddd")








