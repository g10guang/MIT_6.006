#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-01-23 15:24
# 计算有向无环 DAG 图的拓扑结构
# 如果图不是有向无环图，那么不能求得拓扑结构
# 算法：
# 1. 从还没加入拓扑结构的顶点中选取一个入度为 0 的顶点，将该顶点加入拓扑结构，并去除与该顶点相关的所有边，更新每个顶点的入度，重复 1

from course13.graph import DirectGraph, Vertex


class CycleException(Exception):
    """
    图中有环
    """


def topology(dag: DirectGraph):
    """
    求 DAG 的拓扑结构
    :param dag:
    :return:
    """
    indegree = initialize(dag)
    # 顶点加入拓扑结构的顺序
    order = []
    vexnum = dag.get_vertex_num()
    while len(order) < vexnum:
        for v, c in indegree.items():
            if c == 0:
                order.append(v)
                # 更新 -1 代表已经加入了拓扑结果
                indegree[v] = -1
                update(dag, v, indegree)
                break
        else:
            # 图中有环，无法计算该图的拓扑结构
            raise CycleException('图中有环，无法计算该图的拓扑结构')
    return order


def initialize(dag: DirectGraph):
    """
    进行求拓扑结构前的初始化工作
    :param dag:
    :return:
    """
    # 记录每个顶点的入度
    indegree = {v: 0 for v in dag.vertexes}
    for u, pair in dag.edges.items():
        for v, w in pair:
            # 发现 u-->v 更新 v 的入度
            indegree[v] += 1
    return indegree


def update(dag: DirectGraph, v: Vertex, indegree: dict):
    """
    顶点 v 加入到拓扑结构后更新 indegree
    取消所有与 v 相关的入度
    """
    for u, w in dag.edges[v]:
        indegree[u] -= 1


def test_topology():
    dag = DirectGraph()
    a = Vertex('a')
    b = Vertex('b')
    c = Vertex('c')
    d = Vertex('d')
    e = Vertex('e')
    f = Vertex('f')
    g = Vertex('g')
    dag.add_vertex(a)
    dag.add_vertex(b)
    dag.add_vertex(c)
    dag.add_vertex(d)
    dag.add_vertex(e)
    dag.add_vertex(f)
    dag.add_vertex(g)

    dag.add_edge(a, b)
    dag.add_edge(b, c)
    dag.add_edge(c, d)
    dag.add_edge(e, c)
    dag.add_edge(c, g)
    dag.add_edge(c, f)
    dag.add_edge(d, f)

    order = topology(dag)
    print(order)


def test_cycle():
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
    dag.add_vertex(h)
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

    order = topology(dag)
    print(order)

