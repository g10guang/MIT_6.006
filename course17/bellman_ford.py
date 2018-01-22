#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-01-22 16:44
# 使用 Bellman-Ford 算法寻找 DAG 中的 Shortest Path
# Dijkstra 算法在图中如果存在 negative weight cycle 下会无法正确工作
# Bellman-Ford 给予一些推论：
# If a value d[v] fails to converge after |V | − 1 passes, there exists a negative-weight
# cycle reachable from s.

# 伪代码:
# Bellman-Ford(G, W, s):
#     Initialize()
#     for i=1 to |V|:
#         for each edge(u, v) belong to E:
#           Relax(u, v)
#     for each edge(u, v) belong to E:
#         do if d[v] > d[u] + w(u, v)
#             then report a negative weight cycle
import sys

from course13.graph import DirectGraph, Vertex


class NegativeCycleException(Exception):
    """
    发现 negative-cycle 抛出异常
    """
    pass


def bellman_ford(dg: DirectGraph, s: Vertex):
    """
    使用 Bellman-Ford 寻找图中的最短路径
    :param dg: 有向图，其中图中可以存在 negative-weight cycle，Bellman-Ford 算法可以发现 negative-weight cycle
    :param s: 源点 s
    :return:
    """
    # d 用来记录每个顶点距离 s 的最短路径
    # pai 用于记录每个顶点在最短路径中访问的上一个顶点
    d, pai = initialize(dg, s)
    vertex_num = dg.get_vertex_num()
    # 进行 |V| - 1 次循环
    for _ in range(1, vertex_num):
        # 这里从每个顶点开始遍历每一条边
        for u, l in dg.edges.items():
            for v, w in l:
                relax(u, v, w, d, pai)
    try:
        check(dg, d)
    except NegativeCycleException:
        print("图中存在 negative-weight cycle")
    else:
        print("图中不存在 negative-weight cycle")
    return d, pai


def initialize(dg: DirectGraph, s: Vertex):
    """
    对数据进行初始化，这里仅仅初始化 distance dict, pai 记录最路径中访问的上一个顶点
    :param dg:
    :return:
    """
    d = {s: 0}
    pai = {s: None}
    for v in dg.vertexes:
        pai[v] = None
        if v != s:
            d[v] = dg.get_edge_weight(s, v)
            # 使用 sys.maxsize 代表两者之间没有任何关联
            if d[v] < sys.maxsize:
                pai[v] = s
    return d, pai


def relax(u: Vertex, v: Vertex, w, d: dict, pai: dict):
    """
    使用 (u, v) 边更新 d 和 pai
    :param w:
    :param d:
    :param pai:
    :param dg:
    :param u:
    :param v:
    :return:
    """
    if d[v] > d[u] + w:
        d[v] = d[u] + w
        pai[v] = u


def check(dg: DirectGraph, d: dict):
    """
    检查图中是否存在 negative-weight cycle
    :return:
    """
    for u, l in dg.edges.items():
        for v, w in l:
            # 如果图中不存在 negative-cycle 那么 d[v] 应该是最小值
            if d[v] > d[u] + w:
                # 经过 |V| - 1 次迭代后，图中还存在某个顶点的最短路径优化，证明该图中存在 negative-weight cycle
                raise NegativeCycleException("Negative cycle")


def test_bellman_ford():
    dg = DirectGraph()
    a = Vertex('a')
    b = Vertex('b')
    c = Vertex('c')
    d = Vertex('d')
    e = Vertex('e')
    f = Vertex('f')
    g = Vertex('g')
    dg.add_vertex(a)
    dg.add_vertex(b)
    dg.add_vertex(c)
    dg.add_vertex(d)
    dg.add_vertex(e)
    dg.add_vertex(f)
    dg.add_vertex(g)
    dg.add_edge(a, b, 2)
    dg.add_edge(d, a, 3)
    dg.add_edge(b, c, 3)
    dg.add_edge(c, d, 5)
    dg.add_edge(c, e, 6)
    dg.add_edge(c, f, 4)
    dg.add_edge(g, e, -4)
    dg.add_edge(f, g, 2)
    dg.add_edge(b, e, 2)
    dg.add_edge(e, g, 3)

    d, pai = bellman_ford(dg, a)
    print(d, pai)


if __name__ == '__main__':
    test_bellman_ford()
