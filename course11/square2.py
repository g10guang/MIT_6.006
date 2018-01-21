#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-01-20 16:47
# 使用牛顿法计算 根号2 的值，要求精度为 100M 个小数
# 牛顿法的精度是成 2 的倍数指数增长的 1 --> 2 --> 4
# 构造方程 f(x) = x^2 - 2 求解 x 满足 f(x) = 0，该 x = 根号2
# 迭代式：x(i+1) = x(i)/2+1/x(i)

import math


def square2(d):
    """
    计算 d-digit of precision 根号 2
    :param d: 需要多少位精度
    :return:
    """
    # 从 1 位精度小数开始
    result = 1.4
    cal_times = int(log2(d))
    for _ in range(cal_times):
        result = result / 2 + 1 / result
    return result


def log2(d):
    """
    计算 log2 d base is 2
    :param d:
    :return:
    """
    return math.log2(d)


def square(a, d):
    """
    计算 根号a
    x(i+1) = x(i) * 0.5 + a * 0.5 / x(i)
    :param a:
    :param d: 需要的计算精度
    :return:
    """
    # 假设初始计算精度尾　1.0
    result = 1.0
    cal_times = int(log2(d))
    for _ in range(cal_times):
        result = result * 0.5 + a * 0.5 / result
    return result


if __name__ == '__main__':
    # d = square2(10 * 3)
    d = square(3, 10**6)
    print('{:.1000f}'.format(d))
