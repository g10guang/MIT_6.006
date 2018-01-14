#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-07 20:14

# 尽可能使用递归算法实现 BST


class BSTNode:
    """
    Representation of a node in binart search tree
    Has a left child, right child and key value, and stores its subtree size.
    """

    def __init__(self, parent, t) -> None:
        super().__init__()
        self.key = t
        self.parent = parent
        self.key = t
        self.left = None
        self.right = None
        self.size = 1

    def disconnect(self):
        self.parent = None
        self.left = None
        self.right = None

    def update_stats(self):
        """
        Update this nodes's size based on its children's size.
        :return:
        """
        self.size = (0 if self.left is None else self.left.size) + (0 if self.right is None else self.right.size) + 1

    def insert(self, t):
        """
        Insert key t into the subtree rooted at this node (updating subtree size)
        :param t:
        :return:
        """
        # self 子树数量增1
        self.size += 1
        if t < self.key:
            # 应该插在左子树
            if self.left:
                # 递归插到左子树
                self.left.insert(t)
            else:
                self.left = BSTNode(self, t)
        else:
            # 应该插到右子树
            if self.right:
                # 递归插到右子树
                self.right.insert(t)
            else:
                self.right = BSTNode(self, t)

    def find(self, t):
        """
        Returen the node for key t if it is in this tree, or None otherwise
        :param t:
        :return:
        """
        if self.key == t:
            return self
        if self.key < t:
            # 在左子树中寻找
            if self.left:
                return self.left.find(t)
            else:
                return None
        else:
            # 在右子树中寻找
            if self.right:
                return self.right.find(t)
            else:
                return None

    def delete_min(self):
        """
        Delete the minimum key (and return the old node containing it.)
        :return: node, parent
        """
        if self.left or self.right:
            # 树大小减1
            self.size -= 1
            if self.left:
                # 递归从左子树中删除最小节点
                return self.left.delete_min()
            else:
                # 删除该节点，self.right 肯定存在
                # 切换 parent
                self.right.parent = self.parent
                return self, self.parent
        else:
            # 树中只有该节点，直接删除
            self.disconnect()
            return self, None

    def rank(self, t):
        """
        Return the number of keys <= t in the subtree rooted at this node.
        :param t:
        :return:
        """
        left_size = self.left.size if self.left else 0
        if self.key == t:
            return left_size + 1
        elif self.key > t:
            return self.left.rank(t) if self.left else 0
        else:
            return left_size + 1 + self.right.rank() if self.right else 0

    def minimum(self):
        """
        Returns the node with the smallest key in the subtree rooted by this node.
        :return:
        """
        return self.left.minimum() if self.left else self

    def successor(self):
        """
        Returns the node with the smallest key larger than this node's key, or None if this is the largest key in the tree
        :return:
        """
        if self.right:
            # 存在右子树，则寻找右子树的最左下角节点
            return self.right.minimum()
        return None

    def delete(self):
        """
        Delete this node from the tree
        The rule of deleting a node is undefined.
        :return:
        """
        if self.left or self.right:
            # 该节点有左孩子或者右孩子
            pass

    def check(self, lokey, hikey):
        """
        Checks that the subtree rooted at t is a valid BST and all keys are between (lokey, hikey)
        :param lokey:
        :param hikey:
        :return:
        """
        if lokey <= self.key <= hikey:
            if self.parent:
                if self.parent.left is not self and self.parent.right is not self:
                    return False
                if self.parent.left is self.parent.right:
                    return False
            return self.left.check() if self.left else True and self.right.check() if self.right else True
        # 不符合规则
        return False


class BST:
    """
    Simple binary search tree implementation.
    This BST supports insert, find, and delete-min operations.
    Each tree contains some (possibly 0) BSTnode objects, representing nodes.
    and a pointer to the root.
    将关于树的操作传递到节点的操作
    """

    def __init__(self, NodeType=BSTNode) -> None:
        super().__init__()
        self.NodeType = NodeType
        self.psroot = self.NodeType(None, None)

    def reroot(self):
        self.root = self.psroot.left

    def insert(self, t):
        """Insert key t into this BST, modifying it in-place."""
        if self.root is None:
            self.psroot.left = self.NodeType(self.psroot, t)
            self.reroot()
            return self.root
        else:
            # 将操作传递到节点操作
            return self.root.insert(t, self.NodeType)

    def find(self, t):
        """
        Return the node for key t if is in the tree, or None otherwise.
        :param t:
        :return:
        """
        if self.root is None:
            return None
        return self.root.find(t)

    def rank(self, t):
        """
        The number of keys <= t in the tree.
        :param t:
        :return:
        """
        if self.root is None:
            return 0
        return self.root.rank(t)

    def delete(self, t):
        """
        Delete the node for key t if it is in the tree.
        :param t:
        :return:
        """
        node = self.find(t)
        deleted = self.root.delete()
        self.reroot()
        return deleted

    def check(self):
        if self.root is not None:
            return self.root.check()
