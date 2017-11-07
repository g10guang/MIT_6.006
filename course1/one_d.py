#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-31 10:20
# 1-diversion 一位数组的寻找 peak
# 直接算法：从左到右寻找 peak
from tools import mock_data
from tools.count_time import count_time


@count_time
def straight_forward(array):
    # 只有一个元素直接返回 peak
    array_len = len(array)
    if array_len == 1:
        return array[0]
    index = 1
    while index < array_len:
        if array[index] > array[index - 1]:
            if array[index] > array[index + 1]:
                # 找到 peak
                return array[index]
        index += 1


@count_time
def divide_conquer(array):
    array_len = len(array)
    if array_len == 1:
        return array[0]
    # 从中间开始寻找 peak
    index = array_len // 2
    start = 0
    end = array_len
    while start < index < end:
        if array[index] < array[index - 1]:
            # 在左边寻找 peak
            end = index
            index = (end - start) // 2
        elif array[index] < array[index + 1]:
            # 在右边寻找 peak
            start = index
            index = (end - start) // 2
        else:
            # array[index] 就是 peak
            return array[index]


@count_time
def hello():
    print('hello world')


if __name__ == '__main__':
    data = mock_data.mock_array(10**7)
    # print(data)
    result = divide_conquer(data)
    print(result)