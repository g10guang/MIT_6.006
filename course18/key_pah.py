#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-01-23 16:28
# 求图中的关键路径
# AOE（Activity on Edge）假设在工程中，有一系列的活动需要进行，把一些列的活动的顺序以及需要的时间表示为图
# 每一条边代表相应活动所需要的时间，顶点代表事件完成汇聚，代表完成了一系列事件相当于里程碑
# 如果 DAG 不能够生成拓扑结构，那么该 DAG 不存在关键事件，因为该工程矛盾永远不能被完成
# 定义：
# e(i) 活动 i 的最早开始时间
# l(i) 活动 i 的最晚开始时间
# ve(j) 里程碑 j 最早达到时间
# vl(j) 里程碑 j 最晚达到时间
# a(i) 代表弧 <j, k>
# 则满足：
# e(i) = ve(j)
# l(i) = vl(k) - len<j, k>
# 关键活动为 e(i)=l(i) 的活动，证明该活动不能够延时，否则会拖延工期
# 使用拓扑顺序遍历，将拓扑结构的顺序压入栈中，方便后续使用反拓扑结构求 vl：
# 1.从 ve(0) 开始，ve(j) = Max{ve(j) + len<i, j>}
# 2.最后一个里程碑的最早达到时间 == 最晚达到时间，因为工程完成的时间只能有一个，所以有 vl(n-1) = ve(n-1)
# 3.使用反拓扑结构，从栈中一个一个地弹出顶点，求出 vl(i) = Min{vl(j) - len<i, j>}
# 4.找出所有 e(i) == l(i) 的活动，并且标记为关键活动
# 求关键路径的算法：
import sys

from course13.graph import DirectGraph, Vertex
from course18.topology import CycleException


def find_key_path(dag: DirectGraph):
    """
    寻找 DAG 中的关键活动，该算法假设图中不存在 negative weight edge
    """
    stack, vexes, edges, ve, vl, e, l, indegree = initialize(dag)
    # 使用拓扑顺序 ve，并且将拓扑顺序存储在 stack 中
    topological_order(dag, stack, vexes, ve, indegree)
    # stack[-1] 为项目完成的里程碑，最后一个里程碑的最早开始时间==最迟开始时间
    vl[stack[-1]] = ve[stack[-1]]
    # 逆拓扑结构求 vl
    reverse_topology(stack, edges, vl)
    # 计算 e(i) l(i)
    key_path = cal_edge_el(vl, ve, e, l, edges)
    return key_path


def initialize(dag: DirectGraph):
    """
    初始化 stack 栈，初始化各顶点的 ve\vl，初始化各边的 e\i
    :param dag:
    :return:
    """
    # 在 python list 就是一个默认实现的 stack
    stack = []
    vexes = list(dag.vertexes)
    edges = {(u, v): w for u, pair in dag.edges.items() for v, w in pair}
    ve = {v: 0 for v in vexes}
    vl = {v: sys.maxsize for v in vexes}
    e = {x: 0 for x in edges}
    l = {x: sys.maxsize for x in edges}
    # indegree 记录每个顶点的入度，用于 求拓扑结构
    indegree = {v: 0 for v in dag.vertexes}
    for u, pair in dag.edges.items():
        for v, w in pair:
            # 发现 u-->v 更新 v 的入度
            indegree[v] += 1
    return stack, vexes, edges, ve, vl, e, l, indegree


def topological_order(dag: DirectGraph, stack: list, vexes: list, ve: dict, indegree: dict):
    """
    求拓扑结构，并将拓扑顺序保存在栈中，并且求 ve(j) = Max{ve(j) + len<i, j>}
    :param dag:
    :return:
    """
    # 直到所有顶点都已经加入到拓扑结构中
    while len(stack) < len(vexes):
        for v, d in indegree.items():
            if d == 0:
                stack.append(v)
                indegree[v] = -1
                update(dag, indegree, v, ve)
                break
        else:
            raise CycleException('图中有环，无法计算该图的关键路径')


def update(dag: DirectGraph, indegree: dict, v: Vertex, ve: dict):
    """
    当一个新的顶点加入到拓扑结构后，需要进行 indegree 的更新，以及 ve 的更新
    :param dag:
    :param indegree:
    :param v:
    :param ve:
    :return:
    """
    for u, w in dag.edges[v]:
        indegree[u] -= 1
        # ve[u] = Max{ve[u], ve[v] + w}
        if ve[v] + w > ve[u]:
            ve[u] = ve[v] + w


def reverse_topology(stack: list, edges: dict, vl: dict):
    """
    通过逆拓扑结构求 vl
    vl[i] = Min{vl[j] - len<i, j>}
    :param stack:
    :param edges:
    :param vl:
    :return:
    """
    while stack:
        top = stack.pop()
        # 遍历所有以 top 结尾的弧
        for x, y in edges:
            if y == top:
                # 这里虽然新创建了 Edge 对象，但是 Edge 的 hash 只取决于两个顶点对象，所以如果 source target 相同就默认为同一条边
                t = vl[top] - edges[(x, top)]
                if vl[x] > t:
                    vl[x] = t


def cal_edge_el(vl: dict, ve: dict, e: dict, l: dict, edges: dict):
    """
    计算每一条边的 e(i) 最早开始时间和 l(i) 最晚开始时间
    对于每一条边（活动）满足:
    e(i) = ve(j)
    l(i) = vl(k) - len<j, k>
    :return:
    """
    key_path = {}
    # 遍历图中的每一个顶点
    for pair in edges:
        e[pair] = ve[pair[0]]
        l[pair] = vl[pair[1]] - edges[pair]
        # e == l 为关键活动，如果延迟了该活动则整个工期将会被延迟
        if e[pair] == l[pair]:
            key_path[pair] = e[pair]
    return key_path


def test():
    # 以下图中有两条关键路径
    # 1： a-->b-->e-->g-->h
    # 2： a-->b-->e-->f-->h
    dag = DirectGraph()
    a = Vertex('a')
    b = Vertex('b')
    c = Vertex('c')
    d = Vertex('d')
    e = Vertex('e')
    f = Vertex('f')
    g = Vertex('g')
    h = Vertex('h')
    i = Vertex('i')

    dag.add_vertex(a)
    dag.add_vertex(b)
    dag.add_vertex(c)
    dag.add_vertex(d)
    dag.add_vertex(e)
    dag.add_vertex(f)
    dag.add_vertex(g)
    dag.add_vertex(h)
    dag.add_vertex(i)

    dag.add_edge(a, b, 6)
    dag.add_edge(a, c, 4)
    dag.add_edge(a, d, 5)
    dag.add_edge(b, e, 1)
    dag.add_edge(c, e, 1)
    dag.add_edge(d, i, 2)
    dag.add_edge(e, f, 9)
    dag.add_edge(e, g, 7)
    dag.add_edge(f, h, 2)
    dag.add_edge(g, h, 4)
    dag.add_edge(i, g, 4)

    key_path = find_key_path(dag)
    print(key_path)

