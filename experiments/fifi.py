# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 09:45:53 2022

@author: DTEAIAPPS
"""

from collections import deque
import itertools

def moving_average(iterable, n=3):
    # moving_average([40, 30, 50, 46, 39, 44]) --> 40.0 42.0 45.0 43.0
    # http://en.wikipedia.org/wiki/Moving_average
    it = iter(iterable)
    d = deque(itertools.islice(it, n-1))
    d.appendleft(0)
    s = sum(d)
    for elem in it:
        s += elem - d.popleft()
        d.append(elem)
        yield s / n



# avg = moving_average([40, 30, 50, 46, 39, 44])
# print(avg)

x = deque(5*[0], 5)

x.appendleft(1)
x.appendleft(2)
x.appendleft(3)
x.appendleft(4)
x.appendleft(5)
x.appendleft(6)
x.appendleft(7)
