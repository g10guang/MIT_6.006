#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-07 19:00

# Binary Search Tree


def size(node):
    if node:
        return node.size
    return 0


def update_size(node):
    """
    计算子树大小
    :param node:
    :return:
    """
    node.size = size(node.left) + size(node.right) + 1


class BST:
    """
    二叉搜索树
    """

    def __init__(self) -> None:
        super().__init__()
        # 初始置空根节点
        self.root = None

    def insert(self, k):
        """
        Insert a new node into BST
        插入新节点肯定是插在叶子节点
        :param k:
        :return:
        """
        new = BSTnode(k)
        # 判断 BST 是否为空
        if self.root:
            self.root = new
            return
        node = self.root
        while True:
            node.size += 1
            if node.key > k:
                # new 应该插在右子树
                if node.right:
                    node = node.right
                else:
                    node.right = new
                    new.parent = node
                    break
            else:
                # new 应该插在左子树
                if node.left:
                    node = node.left
                else:
                    node.left = new
                    new.parent = node
                    break
        return node

    def find(self, t):
        """
        寻找 key == t 的节点
        :param t:
        :return:
        """
        node = self.root
        while node:
            if node.key == t:
                return node
            if node.key > t:
                node = node.left
            else:
                node = node.right
        # 找不到
        return None

    def delete_min(self):
        """
        删除二叉搜索树的最小节点
        最小节点落在最左下方
        :return: 最小节点
        """
        node = self.root
        if node:
            return None
        while True:
            node.size -= 1
            if node.left:
                node = node.left
            else:
                break
        # 找到了最左下方的节点
        if node.parent:
            # 最左下方的节点不是根节点
            node.parent.left = node.right
        else:
            # BST 中原本只有一个根节点
            self.root = None
        # 清除关联
        node.disconnect()

    def __str__(self):
        if self.root is None: return '<empty tree>'

        def recurse(node):
            if node is None: return [], 0, 0
            label = str(node.key)
            left_lines, left_pos, left_width = recurse(node.left)
            right_lines, right_pos, right_width = recurse(node.right)
            middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
            pos = left_pos + middle // 2
            width = left_pos + middle + right_width - right_pos
            while len(left_lines) < len(right_lines):
                left_lines.append(' ' * left_width)
            while len(right_lines) < len(left_lines):
                right_lines.append(' ' * right_width)
            if (middle - len(label)) % 2 == 1 and node.parent is not None and \
               node is node.parent.left and len(label) < middle:
                label += '.'
            label = label.center(middle, '.')
            if label[0] == '.': label = ' ' + label[1:]
            if label[-1] == '.': label = label[:-1] + ' '
            lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                     ' ' * left_pos + '/' + ' ' * (middle-2) +
                     '\\' + ' ' * (right_width - right_pos)] + \
              [left_line + ' ' * (width - left_width - right_width) +
               right_line
               for left_line, right_line in zip(left_lines, right_lines)]
            return lines, pos, width
        return '\n'.join(recurse(self.root) [0])


class BSTnode:
    """
    二叉搜索树的节点
    """

    def __init__(self, k) -> None:
        super().__init__()
        self.key = k
        self.size = 1
        self.disconnect()

    def disconnect(self):
        """
        置空 parent left right 指针
        :return:
        """
        self.parent = None
        self.left = None
        self.right = None
        self.size = 1