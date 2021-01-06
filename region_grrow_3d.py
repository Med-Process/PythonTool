import os
import numpy as np
import cv2
import copy
import shutil

""""
input: [Z, Y, X]
center: type list, [z, y, x]
"""

class SStack:
    def __init__(self):
        self._elems = [] # 使用list存储栈元素

    def is_empty(self):
        return self._elems == []

    def push(self, elem):
        self._elems.append(elem)

    def pop(self):
        if self._elems == []:
            raise StackUnderflow("in SStack.pop()")
        return self._elems.pop()

    def top(self):
        if self._elems == []:
            raise StackUnderflow("in SStack.top()")
        return self._elems[-1]
    
    def size(self):
        return len(self._elems)


def region_grow_3d(input, center):
    z, y, x = input.shape[0], input.shape[1], input.shape[2]
    seed =  SStack()
    seed.push(center)
    neighber = [[-1,-1,0], [0,-1,0], [1,-1,0], [1,0,0], [1,1,0], [0,1,0], [-1,1,0], [-1,0,0], [0,0,1], [0,0,-1]]
    while seed.size() > 0:
        sz = seed.size()
        pt = seed.top()  # z  y  x
        seed.pop()
        input[pt[0], pt[1], pt[2]] = 2

        for i in range(10):
            temp = neighber[i]
            x_c = temp[0]
            y_c = temp[1]
            z_c = temp[2]
            pz = pt[0] + z_c
            py = pt[1] + y_c
            px = pt[2] + x_c

            if px < 0 or py < 0 or pz < 0 or px > x-1 or py > y-1 or pz > z-1:
                continue

            pixel = input[pz, py, px]

            if pixel == 1:
                ct = [pz, py, px]
                seed.push(ct)
                input[pz, py, px] = 2
    return input
    
    
