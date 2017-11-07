#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-03 20:05

# 归并排序
# 时间复杂度 O(nlogn)
# 空间复杂度 O(nlogn) ==> 使用递归，使用循环可以把空间复杂度降低之 O(n)

from course3.insert_sort import insert_sort, insertion_sort_by_range
from tools.mock_data import mock_array


# def merge_sort2(data):
#     """
#     归并排序
#     :return:
#     """
#     datalen = len(data)
#     datalen_minus_1 = datalen - 1
#     # 用于使用归并 merge
#     duplicate = data.copy()
#     # 粒度
#     granularity = 2
#     while granularity < datalen:
#         # 按照粒度进行划分
#         start = 0
#         while start < datalen_minus_1:
#             # divide
#             end = start + granularity - 1
#             if end >= datalen:
#                 end = datalen
#             # sort
#             insertion_sort_by_range(data, start, end)


def merge_sort(data: list, granularity: int) -> list:
    datalen = len(data)
    if datalen > granularity:
        half_len = datalen // 2
        # divide & sort
        left = merge_sort(data[0: half_len], granularity)
        right = merge_sort(data[half_len:], granularity)
        # merge，从后开始合并
        index = datalen - 1
        while index > 0:
            if left and right:
                if left[-1] > right[-1]:
                    data[index] = left.pop()
                else:
                    data[index] = right.pop()
                index -= 1
            else:
                if left:
                    # right 中的元素已经全部取出，将 left 中剩下的元素全部加入到 data
                    for i, item in enumerate(left):
                        data[i] = item
                else:
                    for i, item in enumerate(right):
                        data[i] = item
                break
        return data
    # granularity >= data 单纯对 data 进行排序
    insert_sort(data)
    return data


def merge_sort_loop(data: list):
    """
    使用循环实现递归排序，降低空间复杂度
    :param data:
    :return:
    """
    datalen = len(data)
    granularity = 2
    while granularity <= datalen:
        start = 0
        # divide
        while start < datalen:
            end = start + granularity
            if end >= datalen:
                end = datalen - 1
            insertion_sort_by_range(data, start, end)
            start += granularity
        # merge
        start = 0
        while start < datalen:
            left = start
            right = start + granularity
            right_end = right + granularity
            if right >= datalen:
                break
            if right_end >= datalen:
                right_end = datalen - 1
            left_list = data[left:right]
            right_list = data[right:right_end]
            li, ri, index = 0, 0, 0
            while li < granularity and ri + right < right_end:
                if left_list[li] <= right_list[ri]:
                    data[start + index] = left_list[li]
                    li += 1
                else:
                    data[start + index] = right_list[ri]
                    ri += 1
                index += 1
            if li < granularity:
                while li < granularity:
                    data[start + index] = left_list[li]
                    li += 1
                    index += 1
            else:
                while ri + right < right_end:
                    data[start + index] = right_list[ri]
                    ri += 1
                    index += 1
            start += granularity * 2
        granularity *= 2
    return data


def main():
    data = mock_array(30)
    granularity = 2
    while granularity < len(data):
        tmp = merge_sort(data, granularity)
        granularity *= 2
    return tmp


def main2():
    data = mock_array(40)
    result = merge_sort_loop(data)
    return result


if __name__ == '__main__':
    result = main2()
    print(result)