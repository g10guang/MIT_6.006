#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-14 19:59
# 为了减少 collision 和 waste
# 需要尽可能提高 hash table 效率


from course8 import abchash
from tools.mathtool import is2power


class ResizableHashTable(abchash.ABCHash):
    """
    为 Hash table 引入可以 grow & shrink，为提高 Hash table 的查询效率和存储效率
    因为 ResizableHashTable 没有实现父类 ABCHash 的抽象方法，所以不能够被实例化
    """

    def __init__(self, m: int=8) -> None:
        # 如果 m 不是 2 的整数次幂，则初始化 m = 8
        if not is2power(m):
            m = 8
        super().__init__(m)

    def _resize(self):
        """
        重新调整大小
        :return:
        """
        if self.elem_num > self.m:
            self._grow()
        elif self.elem_num < self.m // 4:
            if self.m > 8:
                # m <= 8 不收缩
                self._shrink()

    def _grow(self):
        """
        扩张 hash table
        :return:
        """
        old_slot = self.slots
        self.m = self.m * 2
        self.slots = [None] * self.m
        # 迭代 self.slot 然后将值重新计算 hash 插入到新 slot
        self._reinsert(old_slot)

    def _shrink(self):
        """
        缩小 hash table
        :return:
        """
        old_slot = self.slots
        self.m = self.m // 2
        self.slots = [None] * self.m
        self._reinsert(old_slot)

    def _reinsert(self, old_slot):
        """
        将旧的 slot 中内容，复制到新的 slot 中
        :return:
        """
        for item in old_slot:
            while item:
                # 不能够直接像下面调用插入，因为会触发无限迭代
                # self[item.key] = item.value
                hv = self.calhash(item.key)
                if self.slots[hv]:
                    self.slots[hv].insert(item.key, item.value)
                else:
                    self.slots[hv] = abchash.HashNode(item.key, item.value)
                item = item.next


class MHash(ResizableHashTable, abchash.UHash):
    """
    Hash table which can grow & shrink automatically.
    Check every insertion and deletion.
    """

    def __init__(self, m: int = 8) -> None:
        super().__init__(m)

    def __setitem__(self, key, value):
        # 调用父类方法进行插入
        super().__setitem__(key, value)
        super()._resize()

    def __delitem__(self, key):
        # 调用父类方法进行删除
        super().__delitem__(key)
        super()._resize()


if __name__ == '__main__':
    hash_table = MHash()
    for k in range(20):
        hash_table[k] = str(k)
    for item in hash_table:
        print(item)
    print('===========')
    for i in range(15):
        del hash_table[i]
    for item in hash_table:
        print(item)