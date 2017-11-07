#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-07 09:14

# note: 以下全部 data 都是 1-index，以下事例为大根堆
# 原因：
# 某节点 i 其坐孩子为 left(i)=2*i 右孩子为 right(i)=2*i+1

from tools.mock_data import mock_array
import random


def build_max_heap(data: list):
    """
    构建大根堆，时间复杂度为　Ｏ(nlogn)
    :return:
    """
    datalen = len(data)
    for index in range((datalen - 1) // 2, 0, -1):
        max_heapify(data, index)
    return data


def max_heapify(data, i):
    """
    某堆的左右子树均为堆，重新调整为大根堆
    :return:
    """
    datalen = len(data)
    if i > (datalen - 1) // 2:
        # 节点 i 没有孩子
        return
    l = left(i)
    r = right(i)
    largest = l if data[l] > data[i] else i
    if r < datalen:
        if data[r] > data[largest]:
            largest = r
    if i != largest:
        swap(data, i, largest)
        # 递归调用
        max_heapify(data, largest)


def max_heapify_for_sort(data, i, end):
    """
    某堆的左右子树均为堆，重新调整为大根堆
    @:param end: data[end] 为 data 序列中的最后一个元素
    :return:
    """
    if i > end // 2:
        # 节点 i 没有孩子
        return
    l = left(i)
    r = right(i)
    largest = l if data[l] > data[i] else i
    if r <= end:
        if data[r] > data[largest]:
            largest = r
    if i != largest:
        swap(data, i, largest)
        # 递归调用
        max_heapify_for_sort(data, largest, end)


def left(i):
    """
    节点 i 的做孩子
    :param i:
    :return:
    """
    return 2 * i


def right(i):
    """
    节点 i 的右孩子
    :param i:
    :return:
    """
    return 2 * i + 1


def swap(data, i, j):
    """
    交换　data[i] <==> data[j]
    :param data:
    :param j:
    :return:
    """
    data[i], data[j] = data[j], data[i]


def parent(i):
    """
    计算父节点
    :param i:
    :return:
    """
    return i // 2


def is_heap(data):
    """
    判断是否为 heap
    :return:
    """
    datalen = len(data)
    for index in range(1, (datalen - 1) // 2):
        if data[index] < data[left(index)] or data[index] < data[right(index)]:
            return False
    return True


def is_heap_for_sort(data, end):
    """
    判断是否为 heap
    :return:
    """
    for index in range(1, end // 2):
        if data[index] < data[left(index)] or data[index] < data[right(index)]:
            return False
    return True


def insert_node(data: list, node):
    """
    向堆中插入新节点
    """
    data.append(node)
    datalen = len(data)
    # 从下往上调整 heap
    index = datalen - 1
    p = parent(index)
    while p > 0 and data[p] < data[index]:
        swap(data, p, index)
        index = p
        p = parent(p)


def heap_sort(data):
    """
    使用堆排序
    :return:
    """
    # end 记录 data 最后一个元素所在下标
    end = len(data) - 1
    # 1. 将 data 改造成堆
    build_max_heap(data)
    # > 2 因为 data[0] 被忽略，不使用 data[0]
    while end > 1:
        # 第一个元素和堆中最后一个元素交换位置
        swap(data, 1, end)
        # 堆长度 -1
        end -= 1
        # 重新调整堆 O(logn)
        max_heapify_for_sort(data, 1, end)


def main():
    data = mock_array(10000)
    build_max_heap(data)
    # print(data[1:])
    # print(is_heap(data))
    return data


def test():
    for _ in range(10):
        result = main()
        if not is_heap(result):
            print('算法设计失败')


def test_insert():
    for __ in range(100):
        data = mock_array(20000)
        build_max_heap(data)
        for _ in range(100):
            insert_node(data, random.randint(0, 100))
        if not is_heap(data):
            print('算法设计失败')


def test_heap_sort():
    from tools.check import is_sorted
    for _ in range(10):
        data = mock_array(30)
        heap_sort(data)
        print(data[1:], is_sorted(data[1:]))


if __name__ == '__main__':
    test_heap_sort()