#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-14 20:48


def is2power(number):
    """
    判断 number 是否是 2 的整数幂
    :return:
    """
    flag = 0x1
    if number & flag:
        return False
    one_count = 0
    # 判断前 32 位有多少个 1
    for _ in range(1, 32):
        flag <<= 1
        if flag & number:
            one_count += 1
            if one_count > 1:
                return False
    return True if one_count == 1 else False


def how2power(m):
    """
    计算 2 ** n = m
    :param m:
    :return: n
    """
    if not is2power(m):
        raise ValueError('m should be power of 2 but {} is given'.format(m))
    power = 31
    flag = 0x80000000
    while flag:
        if flag & m:
            return power
        else:
            flag >>= 1
            power -= 1


if __name__ == '__main__':
    print(is2power(5))
    print(how2power(8))