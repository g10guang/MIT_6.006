#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-31 11:13
import random


def mock_array(scale):
    """
    随机生成 [0, 20] 长度为 scale 的数组
    :param scale:
    :return:
    """
    return [random.randint(0, 100) for _ in range(scale)]


def mock_2d_matrix(n, m):
    """
    随机生成 m*n 的数组
    :param m:
    :param n:
    :return:
    """
    return [[random.randint(0, 20) for _ in range(m)] for _ in range(n)]


if __name__ == '__main__':
    result = mock_2d_matrix(3, 4)
    print(result)