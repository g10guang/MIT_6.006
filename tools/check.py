#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-07 11:16


def is_sorted(array: list):
    """
    判断 array 是否已经是排好序
    由小到大
    :param array:
    :return:
    """
    for index, item in enumerate(array):
        if index == len(array) - 1:
            break
        if array[index + 1] < item:
            return False
    return True
