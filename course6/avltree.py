#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-10 08:19


class AVLTree:
    def __init__(self, NodeType=AVLNode) -> None:
        super().__init__()
        self.root = None

    def insert(self, k):
        """
        向 AVL T ree 中插入新节点
        :param k:
        :return:
        """
        if self.root:
            self.root.insert(k)
        else:
            self.root = AVLNode(None, k)


class AVLNode:
    def __init__(self, parent, key) -> None:
        super().__init__()
        self.parent = parent
        self.key = key
        self.left = None
        self.right = None
        # self.height = 0     # 没有左右孩子的树的高度为 0
        self.balance = 0    # balance = max_depth(left) - max_depth(right) it should be [-1, 1]

    def disconnect(self):
        """
        接触与父节点、左孩子、右孩子的关系
        :return:
        """
        self.parent = None
        self.left = None
        self.right = None

    def insert(self, k):
        """
        向 AVL Tree 该 node 中插入一个新节点
        导致 AVL 失衡的四种情况:
        1 左孩子的左孩子插入新节点
        2 右孩子的右孩子插入新节点
        3 右孩子的左孩子插入新节点
        4 左孩子的右孩子插入新节点
        :param k:
        :return: 新插入的节点
        """
        if self.key < k:
            # 将 k 插入到左子树
            if self.left:
                new = self.left.insert(k)
            else:
                # 左子树为空，直接插入
                new = AVLNode(self, k)
                self.left = new
        else:
            # 将 k 插入到右子树
            if self.right:
                new = self.right.insert(k)
            else:
                new = AVLNode(self, k)
                self.right = new
        # 更新 balance
        self.balance = self.left.calc_height() if self.left else -1 - self.right.calc_height() if self.right else -1
        self.judge_rotate(new)
        return new

    def judge_rotate(self, new):
        """
        判断二叉树是否失衡，如果失衡采取什么旋转方式
        :return:
        """
        if self.balance == 2:
            if self.left.left is new:
                self.left_rotate()
            elif self.left.right is new:
                self.left_right_rotate()
        elif self.balance == -2:
            if self.right.right is new:
                self.right_rotate()
            elif self.right.left is new:
                self.right_left_rotate()

    def calc_height(self):
        """
        计算该节点的高度
        :return:
        """
        if self.left:
            if self.right:
                return max(self.left.calc_height(), self.right.calc_height()) + 1
            return self.left + 1
        elif self.right:
            return self.right.calc_height() + 1
        else:
            # 没有左孩子，也没有右孩子
            return 0

    def left_rotate(self):
        """
        右子树的右子树插入新节点，导致 AVL 失衡 ==> 单向左旋
        :return:
        """
        right = self.right
        if self.parent:
            if self.parent.left is self:
                self.parent.left = right
            else:
                self.parent.right = right
        right.parent = self.parent
        self.right = right.left
        if right.left_right_rotate():
            right.left.parent = self
        self.parent = right
        right.left = self

    def right_rotate(self):
        """
        左子树的左子树插入新节点，导致 AVL 失衡 ==> 单向右旋
        :return:
        """
        left = self.left
        if self.parent:
            if self.parent.left is self:
                self.parent.left = left
            else:
                self.parent.right = left
        left.parent = self.parent
        self.left = left.right
        if left.right:
            left.right.parent = self
        self.parent = left
        left.right = self

    def left_right_rotate(self):
        """
        左子树的右子树插入新节点，导致 AVL 失衡 ==> 左子树左旋，整体右旋
        :return:
        """
        self.left.left_rotate()
        self.right_rotate()

    def right_left_rotate(self):
        """
        右子树的左子树插入新节点，导致 AVL 失衡 ==> 右子树右旋，整体左旋
        :return:
        """
        self.right.right_rotate()
        self.left_rotate()