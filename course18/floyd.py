#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-01-23 12:04
# 使用 Floyd 算法求每个顶点之间的最短路径
# 求每两个顶点之间的最短路径，其中一种方案是对每一个顶点使用 Dijkstra 算法，时间复杂度为 O(n^3)
# Floyd 算法的思想：从图中编号为 0 的顶点开始，直到遍历所有的顶点，初始 vi --> vj 的最短路径长度为 d(vi, vj)
# 每加入一个新的顶点 vx，就判断 vi-->...-->vx + vx-->...-->vj 路径长度比原来的 d(vi, vj) 更小，如果是则更新
# d(vi, vj) = d(vi, vx) + d(vx, vj)
import sys
import pprint
from course13.graph import DirectGraph, Vertex


def floyd(dag: DirectGraph):
    """
    Floyd 求图中每两个顶点之间的最短路径长度
    :return:
    """
    d, p, vexes, vexnum = initialize(dag)
    # pprint.pprint(vexnum)
    # pprint.pprint(vexes)
    # pprint.pprint(d)
    # pprint.pprint(p)
    for u in range(vexnum):
        for i in range(vexnum):
            for j in range(vexnum):
                if d[i][u] + d[u][j] < d[i][j]:
                    d[i][j] = d[i][u] + d[u][j]
                    for k in range(vexnum):
                        p[i][j][k] = p[i][u][k] or p[u][j][k]
    return d, p, vexes


def initialize(dag: DirectGraph):
    """
    对进行 Floyd 算法求解之前先进行数据的初始化
    :return:
    """
    vexnum = dag.get_vertex_num()
    # Graph 中顶点以　set() 集和存储，这里我们需要将其转化为　list，方便使用下标 index 访问，list 中保存的只是引用，根本上还是 Graph 中 set 的顶点
    vexes = list(dag.vertexes)      # 由于是从 set 转化为 list，所以即使是相同的顶点，生成的 list 每次顶点顺序也可能不一样
    # 用于记录最短路径的关系的三维数组 p
    p = [[[False for _ in range(vexnum)] for j in range(vexnum)] for i in range(vexnum)]
    # 生成用于记录图中每两个顶点之间的最短路径的二维数组 d[i][j] 代表 vi-->vj 的距离
    d = [[dag.get_edge_weight(vexes[i], vexes[j]) if i != j else 0 for j in range(vexnum)] for i in range(vexnum)]
    for i in range(vexnum):
        for j in range(vexnum):
            if d[i][j] < sys.maxsize:
                p[i][j][i], p[i][j][j] = True, True
    return d, p, vexes, vexnum


def test_floyd():
    dag = DirectGraph()
    a = Vertex('a')
    b = Vertex('b')
    c = Vertex('c')
    d = Vertex('d')
    e = Vertex('e')
    f = Vertex('f')
    g = Vertex('g')
    h = Vertex('h')
    dag.add_vertex(a)
    dag.add_vertex(b)
    dag.add_vertex(c)
    dag.add_vertex(d)
    dag.add_vertex(e)
    dag.add_vertex(f)
    dag.add_vertex(g)
    # dag.add_vertex(h)
    dag.add_edge(a, b, 2)
    dag.add_edge(d, a, 3)
    dag.add_edge(b, c, 3)
    dag.add_edge(c, d, 5)
    dag.add_edge(c, e, 6)
    dag.add_edge(c, f, 4)
    dag.add_edge(g, e, 1)
    dag.add_edge(f, g, 2)
    dag.add_edge(b, e, 2)
    dag.add_edge(e, g, 3)
    dag.add_edge(g, c, 3)
    d, p, vexes = floyd(dag)
    pprint.pprint(vexes)
    pprint.pprint(d)
    pprint.pprint(p)


if __name__ == '__main__':
    test_floyd()
