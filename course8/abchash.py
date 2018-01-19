#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-11 13:28
import abc
import pickle
import random

import math
from tools.mathtool import how2power


class HashNode:
    """
    Hash 表中元素，模拟链表中元素
    """

    def __init__(self, key, value, next_elem=None) -> None:
        """
        :param next_elem: 下一个元素的引用
        :param key: 元素键
        :param value: 元素值
        """
        super().__init__()
        self.key = key
        self.value = value
        self.next = next_elem

    def find(self, key):
        """
        在链表中递归寻找元素 key
        :param key:
        :return:
        """
        if self.key == key:
            return self.value
        elif self.next:
            return self.next.find(key)
        else:
            raise KeyError('key "{}" is not exists'.format(key))

    def delete(self, key):
        """
        删除链表中某个元素
        :return: 返回被删除的元素
        """
        if self.key == key:
            return self
        elif self.next:
            result = self.next.delete(key)
            if result is self.next:
                # 如果递归结果返回是，该节点的下一级节点被删除，则更新 self 节点的 next 指向
                self.next = self.next.next
            return result

    def insert(self, key, value):
        """
        将新元素插入到最末尾
        :param key:
        :param value: 
        :return: 新插入到链表中的节点
        """
        if self.key == key:
            new_node = self.value = value
        elif self.next:
            new_node = self.next.insert(key, value)
        else:
            # 到最后一个节点
            new_node = HashNode(key, value)
            self.next = new_node
        return new_node

    def __repr__(self) -> str:
        return 'key={} value={}'.format(self.key, self.value)


class ABCHash(abc.ABC):
    """
    声明 MHash 为抽象类，相当于定义 Hash 类的接口
    """

    def __init__(self, m: int) -> None:
        """
        :param m: 数组的长度
        """
        super().__init__()
        # m 记录　hash table 中 slot 中数目
        self.m = m
        self.slots = [None, ] * m
        # 用于记录 hash table 中已有元素个数
        self.elem_num = 0

    @abc.abstractmethod
    def calhash(self, key) -> int:
        """
        计算 key 的 hash 值(prehashing)
        if key is None: return 0
        :param key:
        :return:
        """
        pass

    def __getitem__(self, key):
        """
        直接使用 obj[key] 去取对象
        :param key:
        :return:
        """
        # 计算 Hash 值
        hv = self.calhash(key)
        if self.slots[hv]:
            # 该位置已有元素，需要在链表中插入元素
            return self.slots[hv].find(key)
        else:
            raise KeyError('key "{}" is not exists'.format(key))

    def __setitem__(self, key, value):
        """
        直接使用 obj[key] = xxxx 来赋值
        :param key:
        :param value:
        :return:
        """
        hv = self.calhash(key)
        if self.slots[hv]:
            self.slots[hv].insert(key, value)
        else:
            # 对应位置还没有元素，直接插入
            self.slots[hv] = HashNode(key, value)
        # 元素个数　+ 1
        self.elem_num += 1

    def __delitem__(self, key):
        """
        从 hash table 中删除某个元素
        :param key:
        :return:
        """
        hv = self.calhash(key)
        if self.slots[hv]:
            deleted_node = self.slots[hv].delete(key)
            # 如果删除的是第一个元素
            if deleted_node is self.slots[hv]:
                self.slots[hv] = deleted_node.next
            self.elem_num -= 1
        else:
            raise KeyError('key "{}" is not exists'.format(key))

    def __iter__(self):
        """
        递归 self.slots
        :return:
        """
        self.__last = None
        return self

    def __next__(self):
        """
        一直迭代
        :return:
        """
        if self.__last:
            if self.__last.next:
                self.__last = self.__last.next
            else:
                hv = self.calhash(self.__last.key)
                hv += 1
                while hv < self.m and not self.slots[hv]:
                    # 该 slot 位置没有任何元素
                    hv += 1
                if hv >= self.m:
                    # 迭代结束
                    raise StopIteration
                else:
                    # 继续迭代
                    self.__last = self.slots[hv]
        else:
            hv = 0
            # 开启第一次迭代
            if self.slots:
                while hv < self.m and not self.slots[hv]:
                    # 该 slot 位置没有任何元素
                    hv += 1
                if hv >= self.m:
                    # 结束迭代
                    raise StopIteration
                else:
                    self.__last = self.slots[hv]
        # 返回迭代对象
        return self.__last

    def __len__(self):
        return self.elem_num


class DHash(ABCHash):
    """
    使用 Division method 计算 hash 值
    h(k) = k mod m
    """

    def __init__(self, m: int) -> None:
        super().__init__(m)

    def calhash(self, key):
        """
        h(k) = k mod m
        :param key:
        :return:
        """
        if key is None:
            # 插在第 0 位
            return 0
        num = obj2int(key)
        # 计算 Hash 值
        return num % self.m


class MHash(ABCHash):
    """
    使用 multiplication method:
    h(k) = [(a * k) % 2 ** w] >> (w - r)
    其中 w 为 bit 长度
    r < w
    a 为随机数
    k 为转化为 int 后的键值
    """

    def __init__(self, m: int) -> None:
        super().__init__(m)
        self.r = how2power(m)

    def calhash(self, key):
        """
            使用 multiplication method:
            h(k) = [(a * k) % (2 ** w)] >> (w - r)
            其中 w 为 bit 长度
            m = 2 ** r
            r < w
            a 为随机数
            k 为转化为 int 后的键值
        :param key:
        :return:
        """
        if key is None:
            return 0
        k = obj2int(key)
        # 计算 k 的位长度
        w = k.bit_length()
        a = random.getrandbits(w)
        return ((a * k) % (w ** 2)) >> (w - self.r)


class UHash(ABCHash):
    """
    Universal Hashing
    h(k) = [(a * k + b) % p] % m
    a & b are both random number
    p is a big prime, which larger than the size of key set.
    """

    def __init__(self, m: int) -> None:
        super().__init__(m)
        self.a = random.randint(0, 2 ** 32)
        self.b = random.randint(0, 2 ** 32)
        # 大素数
        self.p = 89826991

    def calhash(self, key):
        """
        Universal method:
        h(k) = [(a * k + b) % p] % m
        :param key:
        :return:
        """
        if key is None:
            return 0
        k = obj2int(key)
        return ((self.a * k + self.b) % self.p) % self.m


def obj2int(key):
    """
    使用 pickle 转化 object 为 bytes
    """
    try:
        b = pickle.dumps(key)
    except RecursionError as e:
        print(e)
    # 将 bytes 转化为十六进制的字符串
    hexi = b.hex()
    # 将十六进制的字符串转化为 int 整形
    return int(hexi, 16)


if __name__ == '__main__':
    dh = UHash(11)
    for i in range(100):
        dh[i] = str(i)
    for i in range(100):
        if i % 2:
            del dh[i]
    # for i in range(100):
    #     if not i % 2:
    #         print(dh[i])
    num = 0
    for item in dh:
        print(item)
        num += 1
    print(num)
    print(len(dh))
    # print(dh['hello'], dh['world'])

