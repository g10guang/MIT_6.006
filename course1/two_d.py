#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-31 11:11
from tools.mock_data import mock_2d_matrix
from tools.count_time import count_time


@count_time
def greedy_ascent(array):
    """
    贪心递增，每次寻找最大值所在的方向前进
    :param array:
    :return:
    """
    n = len(array)
    m = len(array[0])
    row = n // 2
    col = m // 2
    tmp_row, tmp_col = 0, 0
    tmp_max = array[row][col]
    while 0 < col < m - 1 and 0 < row < n - 1:
        # 寻找最大值方向
        if tmp_max < array[row][col - 1]:
            tmp_max = array[row][col - 1]
            tmp_row = row
            tmp_col = col - 1
        if tmp_max < array[row][col + 1]:
            tmp_max = array[row][col + 1]
            tmp_row = row
            tmp_col = col + 1
        if tmp_max < array[row - 1][col]:
            tmp_max = array[row - 1][col]
            tmp_row = row - 1
            tmp_col = col
        if tmp_max < array[row + 1][col]:
            tmp_max = array[row + 1][col]
            tmp_row = row + 1
            tmp_col = col
        if tmp_max == array[row][col]:
            # 找到　peak
            return tmp_max
        # 继续沿着最大值方向寻找
        col = tmp_col
        row = tmp_row
        tmp_max = array[row][col]


def expand_1d_conquer_2d(array):
    """
    使用分治法，将二维问题先转化为一维问题，然后逐个破解
    方法：
    1. 从中间列开始，寻找该列的最大值（global maximum）
    2. 将 global maximum 与左右两列同一行的值进行比较
    3. 如果 global maximum 比左右列对应行大，则 global maximum 为 peak
    4. 否则如果分别在左右开始搜索 peak
    :param array:
    :return:
    """
    n = len(array)
    m = len(array[0])
    row = n // 2        # 从中间行开始搜索
    start, end = 0, n - 1   # 搜索行范围
    # 一直搜索，直到只剩下一行
    while end != start:
        tmp_index, tmp_max = find_array_global_maximum(array[row])
        if tmp_max < array[row - 1][tmp_index]:
            # 缩小搜索范围
            end = row - 1
            row = (end - start) // 2
        elif tmp_max < array[row + 1]:
            # 缩小搜索范围
            start = row + 1
            row = (end - start) // 2
        else:
            # 找到了 peak
            return tmp_max
    # 搜索最后只剩下一行，则该行的最大值就是 peak
    return max(array[end])


def find_array_global_maximum(array):
    """
    搜索数组的全局最大值，时间复杂度 O(n)
    :param array:
    :return:
    """
    tmp_max = array[0]
    index = 0
    for i, item in enumerate(array):
        if item > tmp_max:
            index = i
            tmp_max = item
    return index, tmp_max


if __name__ == '__main__':
    data = mock_2d_matrix(200, 200)
    result = greedy_ascent(data)
    print(result)