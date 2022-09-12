# -*- coding: utf-8 -*-
"""
Created on Fri May 27 09:39:13 2022

@author: DTEAIAPPS
"""

import random

N = 5


lat = [random.random()+30 for i in range(N)]

lon = [random.random()+70 for i in range(N)]

new_lat = []
for idx, ele in enumerate(lat):
    new_lat.append(ele)
    if idx!= 0 and idx%4 ==0:
        new_lat.append(new_lat[-4])
        new_lat.append(None)

new_lon = []
for idx, ele in enumerate(lon):
    new_lon.append(ele)
    if idx!= 0 and idx%4 ==0:
        new_lon.append(new_lon[-4])
        new_lon.append(None)
