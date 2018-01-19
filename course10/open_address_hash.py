#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-01-14 20:50
# 使用 open addressing 来解决 hash 冲突问题
# open addressing: 更加有效地利用内存，不需要处理链表指针
# 但是 open addressing 对 hash 函数要求更高，从而达到巡逻时的均衡，避免发生 cluster 聚集效应
# open addressing 需要保证 m >= n，这就涉及到什么时候扩容 m，什么时候收缩 m
# 关键在于确定一个好的 probe(k,i) 用于保证插入和搜索效率，防止像线性搜索一样出现 cluster 聚集效应

import abc
import random
from enum import Enum

from course8.abchash import obj2int


class SlotStatus(Enum):
    """
    用于标记 Slot 的状态，分别有：
    Empty: 空的，尚未被插入任何数据
    Delete: 该 slot 中原有的数据已经被删除
    Occupied: slot 已经被元素占有
    """
    Empty = 1
    Deleted = 2
    Occupied = 3


class SlotItem(object):
    """
    Hash 中 slot 的状态
    """

    def __init__(self, status=SlotStatus.Empty, key=None, value=None) -> None:
        super().__init__()
        self.status = status
        self.key = key
        self.value = value

    def update(self, status, key, value):
        """
        更新 slot item 状态和值
        :param status:
        :param key:
        :param value:
        :return:
        """
        self.status = status
        self.key = key
        self.value = value

    def __repr__(self):
        return 'status: {} key: {} value: {}'.format(self.status, self.key, self.value)


class OpenAddressHash(abc.ABC):
    """
    声明抽象的使用 Open address 方法的 Hash
    """

    def __init__(self) -> None:
        super().__init__()
        # 代表 slot 数量，也就是使用数组的大小
        self.m = 8
        # 代表现在 slot 中已经插入的数量
        self.n = 0
        # 以下生成固定长度的 list 会有可能引发引用复制问题，参考https://stackoverflow.com/a/34374129/7159205
        # self.slot = [SlotItem(), ] * self.m
        # 可以使用列表生成式
        self.slot = [SlotItem() for _ in range(self.m)]

    @abc.abstractmethod
    def probe(self, h, i) -> int:
        """
        probe 巡逻直到找到适合的位置，然后将数据插入其中
        :return:
        """
        pass

    @abc.abstractmethod
    def hash(self, key):
        """
        计算 hash
        :param key:
        :return:
        """

    def insert(self, key, value):
        """
        插入
        :param key:
        :param value:
        :return:
        """
        for i in range(self.m):
            h = self.hash(key)
            pos = self.probe(h, i)
            item = self.slot[pos]
            if item.status == SlotStatus.Occupied:
                # 该位置已经被占有，需要 probe 下一个位置
                if item.key == key:
                    # key 相同，则替换原来的值
                    # 这种情况不需要 self.n += 1 操作，只是属于 update 操作
                    item.value = value
                    return
            else:
                # Empty or Deleted 可以直接将元素插入到该位置
                item.update(SlotStatus.Occupied, key, value)
                self.n += 1
                # 最后调用 grow() 判断是否需要扩容
                self.grow()
                return
        else:
            # 巡逻了所有位置都没有找到合适的插入点
            self.grow()
            # 重新进行插入操作
            self.insert(key, value)

    def grow(self):
        """
        扩容，将所有元素重新插入
        触发扩容的条件是 self.n > self.m // 2
        :return:
        0 ==> 需要扩容，并执行了相应的扩容
        1 ==> 不需要扩容，没有进行任何元素
        """
        if self.n <= self.m // 2:
            # 如果插入的元素多于一半，就扩容
            return 1
        old_m = self.m
        old_slot = self.slot
        self.m = old_m * 2
        self.slot = [SlotItem() for _ in range(self.m)]
        # 因为下面重新调用 insert 会造成 self.n 不断地增长
        self.n = 0
        for item in old_slot:
            # 重新将未删除的元素插入到新的 slot 槽中
            if item.status == SlotStatus.Occupied:
                self.insert(item.key, item.value)
        return 0

    def shrink(self):
        """
        收缩，同样将所有元素重新插入到新的 slot 中
        :return:
        0 ==> 需要收缩，并执行了相应的收缩
        1 ==> 不需要收缩，没有进行任何操作
        """
        # 设置 self.m <= 8 是防止 slot 太小
        if self.n >= self.m // 4 or self.m <= 8:
            return 1
        old_m = self.m
        old_slot = self.slot
        self.m = old_m // 2
        self.slot = [SlotItem() for _ in range(self.m)]
        # 这里 self.n = 0 不会造成 slot 的收缩，因为下面调用 insert 操作，不会触发 shrink 操作
        self.n = 0
        for item in old_slot:
            # 重新将未删除的元素插入到新的 slot 槽中
            if item.status == SlotStatus.Occupied:
                self.insert(item.key, item.value)
        return 0

    def delete(self, key):
        """
        从 hash 中删除某个 key 值
        :param key:
        :return:
        """
        for i in range(self.m):
            h = self.hash(key)
            pos = self.probe(h, i)
            item = self.slot[pos]
            if item.status == SlotStatus.Empty:
                # 宣布删除失败，因为该元素不存在与 hash 中
                raise KeyError('No key: {}'.format(key))
            elif item.status == SlotStatus.Deleted:
                # 原有的元素已经被删除，直接巡逻下一个位置
                continue
            else:
                # Occupied
                if item.key == key:
                    item.status = SlotStatus.Deleted
                    # 元素数量 -1
                    self.n -= 1
                    # 判断是否需要收缩
                    self.shrink()
                    return
        else:
            # 巡逻了所有的 slot 都没有找到该元素，所以 key 不存在于 hash 中
            raise KeyError('No key: {}'.format(key))

    def __getitem__(self, key):
        """
        使用类似 Python build-in dict 方式获取 item
        :param key:
        :return:
        """
        for i in range(self.m):
            h = self.hash(key)
            pos = self.probe(h, i)
            item = self.slot[pos]
            if item.status == SlotStatus.Occupied:
                if item.key == key:
                    return item.value
        else:
            raise KeyError('No key: {}'.format(key))

    def __setitem__(self, key, value):
        """
        使用类似 python build-in 字典插入数据
        :param key:
        :param value:
        :return:
        """
        self.insert(key, value)

    def __delitem__(self, key):
        """
        使用类似 python build-in 字典删除数据
        :param key:
        :return:
        """
        self.delete(key)

    def __repr__(self):
        l = ['m: {} n: {}'.format(self.m, self.n)]
        for index, item in enumerate(self.slot):
            if item.status == SlotStatus.Occupied:
                l.append('pos: {} {}'.format(index, repr(item)))
        return '\n'.join(l)


class LinearHash(OpenAddressHash):
    """
    使用线性 probe 方法的 open address hash
    """
    def __init__(self):
        super().__init__()
        # 以下参数用于计算 hash
        self.a = random.randint(0, 2 ** 32)
        self.b = random.randint(0, 2 ** 32)
        # 大素数
        self.p = 89826991

    def probe(self, h, i) -> int:
        return (h + i) % self.m

    def hash(self, key):
        """
        计算 probe 用的 hash
        Universal Hashing
        h(k) = [(a * k + b) % p] % m
        a & b are both random number
        p is a big prime, which larger than the size of key set.
        :param key:
        :return:
        """
        k = obj2int(key)
        return ((self.a * k + self.b) % self.p) % self.m


class DoubleHash(OpenAddressHash):
    """
    使用两个hash函数的方法来 probe
    probe(k, i) = (h1(k) + i * h2(k)) % m
    """

    def hash(self, key):
        hi = obj2int(key)
        return self.h1(hi), self.h2(hi)

    def __init__(self):
        super().__init__()
        # 以下参数用于计算 hash
        self.a1 = random.randint(0, 2 ** 32)
        self.b1 = random.randint(0, 2 ** 32)
        # 大素数
        self.p1 = 89826991
        self.a2 = random.randint(0, 2 ** 32)
        self.b2 = random.randint(0, 2 ** 32)
        # 大素数
        self.p2 = 89826991

    def h1(self, hi):
        """
        第一次 hash
        :param hi:
        :return:
        """
        return ((self.a1 * hi + self.b1) % self.p1) % self.m

    def h2(self, hi):
        """
        第二次 hash
        :param hi:
        :return:
        """
        return ((self.a2 * hi + self.b2) % self.p2) % self.m

    def probe(self, h, i) -> int:
        return (h[0] + h[1] * i) % self.m


def test_linear():
    lh = LinearHash()
    for i in range(15):
        lh[chr(ord('a') + i)] = i
    for i in range(8):
        del lh[chr(ord('a') + i)]
    print(lh)


def test_Double():
    dh = DoubleHash()
    for i in range(15):
        dh[chr(ord('a') + i)] = i
    for i in range(8):
        del dh[chr(ord('a') + i)]
    print(dh)


if __name__ == '__main__':
    test_Double()
