#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-02 18:30

# 输入两个文件，计算两个文件的相似度

import sys
import re
from collections import Counter
import math


def read_file(filename):
    """
    读取文件，该方法不适用于大文件，因为可以需要消耗过多内存
    当使用大文件时，最好逐行读取文件内容
    :param filename:
    :return:
    """
    try:
        with open(filename) as f:
            return f.read()
    except IOError:
        print('Error opening or reading input file.')
        sys.exit()


def count_frequency(content):
    """
    计算文件的单词出现次数，使用正则表达式进行匹配
    :return:
    """
    result = re.findall(r'\w+', content)
    c = Counter()
    for word in result:
        c[word] += 1
    return c


def inner_product(d1, d2):
    """
    计算两个向量的乘积
    :param d1:
    :param d2:
    :return:
    """
    result = 0
    for k, v in d1.items():
        result += v * d2[k]
    return result


def norm(d):
    """
    计算一个向量的长度
    :param d:
    :return:
    """
    return sum(map(lambda x: d[x] * d[x], d))


def cal_words_list(string):
    """
    把字符串中的单词统计出来
    :return:
    """
    words_list = []
    letters_list = []
    for ch in string:
        # if 65 <= ord(ch) <= 90 or 97 <= ord(ch) <= 122:
        if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
            letters_list.append(ch)
        elif letters_list:
            # 将字符连接起来，并且转化为小写
            words_list.append(''.join(letters_list).lower())
            letters_list.clear()
    # 判断是否 string 是以英文字母结束的
    if letters_list:
        words_list.append(''.join(letters_list).lower())
    return words_list


def main():
    """
    主函数入口
    :return:
    """
    filename1 = input('输入第一个文件名: ')
    filename2 = input('输入第二个文件名: ')
    # filename1, filename2 = sys.argv[1], sys.argv[2]
    doc1 = read_file(filename1)
    doc2 = read_file(filename2)
    fre1 = count_frequency(doc1)
    fre2 = count_frequency(doc2)
    result = math.acos(inner_product(fre1, fre2) / math.sqrt(norm(fre1) * norm(fre2)))
    print('Similarity is {}'.format(result))


if __name__ == '__main__':
    # main()
    result = cal_words_list('hello world12 你好吗 haha 2343 32 hello')
    print(result)