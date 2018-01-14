#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-31 10:43

import time
import functools


def count_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        consume = time.time() - start
        print('consume {}s'.format(consume))
        return result
    return wrapper
