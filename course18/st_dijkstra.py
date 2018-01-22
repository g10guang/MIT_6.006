#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-01-22 20:02
# 如果在图中需要搜索的目标是 single-source s and single-target t，那么可以对 Dijkstra 算法进行优化
# 如果新加入 S 的顶点为 t，那么可以停止搜索


import sys

from course13.graph import DirectGraph, Vertex


def dijkstra_single_source_single_target(dg: DirectGraph, s: Vertex, t: Vertex):
    """
    使用 Dijkstra 遍历有向无环图，假设该图为有向无环图 DAG，以下代码不做判断
    寻找 DAG 中 s-->t 的最短路径
    :param dg: course13.graph.DirectGraph
    :param s: 寻找DAG中所有顶点到 s 的最短路径 S.P
    :param t: 目标顶点
    :return:
    """
    if not dg.has_vertex(s):
        print(dg)
        raise Exception("顶点: {} 不在 DAG 中")
    # S 为已经找到最短路径的顶点
    # Q 为尚未找到最短路径的顶点
    # d 为对应目前迭代中该顶点到 s 的距离
    # pai 用于记录在最短路径中，该顶点的上一个顶点
    S, Q, d, pai = initialize(dg, s)
    while Q:
        # extract-min from Q
        v, minimize = extract_min(Q, d)
        # 如果 v == t 那么可以停止搜索，已经找到了目标 s-->t 最短路径
        if v == t:
            S.add(v)
            Q.remove(v)
            break
        if v is not None:
            S.add(v)
            Q.remove(v)
            relax(dg, d, pai, v)
        else:
            # 所有可以被 S 达到的顶点都已经被遍历，剩下的顶点无法从 s 到达
            # 有可能 s-x->t 不存在这样的路径，也就是 d[t] = sys.maxsize
            break
    return d, pai


def initialize(dg: DirectGraph, s):
    """
    在进行 Dijkstra 算法前先进行初始化数据
    :param dg:
    :param s:
    :return:
    """
    # 所有已经找到了最短路径的顶点集和
    S = {s}
    # 所有还没有找到最短路径的顶点集和
    Q = set()
    d = {s: 0}
    pai = {s: None}
    # 将所有非 s 顶点加入到 Q 中
    for v in dg.vertexes:
        pai[v] = None
        if v != s:
            Q.add(v)
            d[v] = dg.get_edge_weight(s, v)
            if d[v] < sys.maxsize:
                pai[v] = s
    return S, Q, d, pai


def extract_min(Q, d) -> (Vertex, int):
    """
    从 Q 中寻找 d[v] 最小者
    在这里如果 Q 不是 set，而是 min heap 最小堆，那么该算法将会得到更优的结果，使用 Fibonacci heap 会得到更加优化的结果
    因为 extract_min 是该算法中的性能热点，每次都要执行，而且如果是 set 的弧每次时间复杂度是 O(n)
    :param Q:
    :param d:
    :return:
    """
    minimize = sys.maxsize
    v = None
    for x in Q:
        if minimize > d[x]:
            minimize = d[x]
            v = x
    return v, minimize


def relax(dg: DirectGraph, d: dict, pai: dict, v: Vertex):
    """
    加入新的顶点到 S 后，更新 d
    :param dg:
    :param d:
    :param v: 新加入的顶点
    :param pai:
    :return:
    """
    for x, weight in dg.edges[v]:
        if d[x] > d[v] + weight:
            d[x] = d[v] + weight
            # 即使当前找到的 v-->x 不是最优路径，但是如果存在最优路径 y-->x，那么后面也绝对会再次更新 pai，所以 Dijkstra 算法结束后，
            # 一定得到 pai[x] 是在最短路径中 x 的上一个顶点，Dijkstra 是一个贪心算法，不断地趋近最优解
            pai[x] = v


def print_shortest_path(pai: dict, s: Vertex, t: Vertex):
    """
    在控制台输出最短路径
    :param pai: 记录这每个顶点的上一个访问顶点
    :param s: 源点 source
    :param t: 目标 target
    :return:
    """
    if not pai[t]:
        # 不存在路径 s-->t
        print('path from {s} to {t} is not exist'.format(s=repr(s), t=repr(t)))
    else:
        print_path(pai, t)
        print(t)


def print_path(pai: dict, v: Vertex):
    """
    递归调用打印输出路径
    :param pai:
    :param v:
    :return:
    """
    if pai[v]:
        print_path(pai, pai[v])
        print(pai[v], end='-->')


def test_dijkstra_single_source_single_target():
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
    dg.add_edge(g, e, 1)
    dg.add_edge(f, g, 2)
    dg.add_edge(b, e, 2)
    dg.add_edge(e, g, 3)

    s, t = a, g

    d, pai = dijkstra_single_source_single_target(dg, s, t)
    print(d, pai)
    print('=======')
    print_shortest_path(pai, s, t)


if __name__ == '__main__':
    test_dijkstra_single_source_single_target()