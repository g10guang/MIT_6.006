#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-01-23 15:09
# 使用动态规划 Dynamic programming to solve Fibonacci number


def navie_fib(n):
    """
    最简单的递归解决 Fibonacci 问题
    :return:
    """
    if n <= 2:
        return 1
    else:
        return navie_fib(n - 1) + navie_fib(n - 2)


def memoize_fib(n, fib={}):
    """
    把计算过程保留 memoize，这样能够 reuse 减少重复计算
    :param n:
    :return:
    """
    if n in fib:
        return fib[n]
    if n <= 2:
        f = 1
    else:
        f = memoize_fib(n - 1, fib) + memoize_fib(n - 2, fib)
    fib[n] = f
    return f


def bottom_up_fib(n):
    """
    不适用递归，可以转化为从底层开始计算，因为从底层计算更加容易实现计算结果的复用
    :param n:
    :return:
    """
    fib = {}
    for i in range(1, n + 1):
        if i <= 2:
            fib[i] = 1
        else:
            fib[i] = fib[i - 1] + fib[i - 2]
    return fib[n]


def test():
    import time
    start = time.time()
    n = 40
    p1 = navie_fib(n)
    end = time.time()
    print('navie consume:', end - start)
    start = time.time()
    p2 = memoize_fib(n)
    end = time.time()
    print('memoize consume:', end - start)
    start = time.time()
    p3 = bottom_up_fib(n)
    end = time.time()
    print('bottom up consume:', end - start)
    assert p1 == p2 == p3


if __name__ == '__main__':
    test()