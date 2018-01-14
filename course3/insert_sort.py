#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-03 19:07

# 插入排序


def insert_sort(data):
    """
    普通插入排序
    :return:
    """
    for index, item in enumerate(data):
        # 元素更小，应该往后移动
        while index > 0 and item < data[index - 1]:
            data[index] = data[index - 1]
            index -= 1
        # 找到插入位置，直接插入
        data[index] = item
    return data


def binary_insertion_sort(data):
    """
    插入排序，使用二分查找进行比较
    如果比较操作比较耗时，那么使用二分查找，寻找插入位置是一个更好方案 O(n) ==> O(logn)
    Complexity:  O(nlogn) comparisions (n square) swaps
    :param data:
    :return:
    """
    for index, item in enumerate(data):
        insert_position = binary_compare(data, index, item)
        for t in range(index - insert_position):
            # 元素向后移动一位
            data[index - t] = data[index - t - 1]
        # 将元素插入到对应位置
        data[insert_position] = item
    return data


def binary_compare(data, end, target):
    """
    对 data[start:end] 进行比较，前闭后开
    :param data:
    :param end:
    :return: target 应该插入到 start 的位置
    """
    start = 0
    while start < end:
        mid = (end + start) // 2
        if data[mid] <= target:
            if start == mid:
                # 该情况下，end - start = 1
                return end
            start = mid
        else:
            if start == mid:
                return start
            end = mid
    # 该返回值只会发生在 end == 0 情况下，第一次返回
    return end


def insertion_sort_by_range(data, start, end):
    """
    按照下标进行 inner sort    [start, end] 两边都闭合
    :param data:
    :param start:
    :param end:
    :return:
    """
    for index in range(start, end + 1):
        item = data[index]
        while index > start and item < data[index - 1]:
            data[index] = data[index - 1]
            index -= 1
        data[index] = item


if __name__ == '__main__':
    from tools.mock_data import mock_array

    data = mock_array(20)

    print('排序前: ', data)

    # binary_insertion_sort(data)

    insertion_sort_by_range(data, 10, 19)

    print('排序后: ', data)
