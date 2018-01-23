#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-01-22 19:59
# 如果在图中需要搜索的目标是 single-source s and single-target t，那么可以对 Dijkstra 算法进行优化
# 从 s 开始进行 forward Dijkstra search；从 t 开始进行 backward Dijkstra search
# Qf df 分别表示 forward search 中尚未确定的顶点、df 表示当前其他结点到 s 的距离
# Qb db 分别表示 backward search 中尚未确定的顶点、db 表示当前其他结点到 t 的最短路径
# 判断停止的方法是：如果一个顶点已经在 Qf 和 Qb 中去除了，那么判断 df[w] + db[w] <= df[x] + db[x]
# 其中 x 为其他在 Qf | Qb 并集中任意一个顶点
import sys

from course13.graph import DirectGraph, Vertex
from course16.dijkstra import extract_min, relax


class NoPathException(Exception):
    """
    当使用 bi_dijkstra() 方法时，如果不存在 s-x->t 的路径，那么就抛出该异常
    """
    pass


def bi_dijkstra(dag: DirectGraph, s: Vertex, t: Vertex):
    """
    使用变种的 Dijkstra 算法求顶点 s 到顶点 t的最短路径
    :param dag: 有向无环图
    :param s: 源点
    :param t: 目标顶点
    :return:
    """
    Sf, Sb, Qf, Qb, df, db, paif, paib = initialize(dag, s, t)
    flag = False
    fn = s
    bn = t
    while Qf:
        flag = not flag
        if flag:
            n = forward(dag, Sf, Qf, df, paif)
            fn = n
        else:
            n = backward(dag, Sb, Qb, db, paib)
            bn = n
        if fn is None and bn is None:
            # 证明 s-x->t 路径不存在
            raise NoPathException('不存在路径 {s}-->{t}'.format(s=s, t=t))
        if n is not None:
            if n not in Qf and n not in Qb:
                if judge(dag, df, db, n):
                    # 成功找到最短路径
                    return df, db, paif, paib, n
                else:
                    # 该顶点 n 不是最短路径上的顶点
                    continue


def forward(dag: DirectGraph, Sf: set, Qf: set, df: dict, paif: dict):
    """
    向前搜索 fom s
    :return:
    """
    v, minimize = extract_min(Qf, df)
    if v is not None:
        Sf.add(v)
        Qf.remove(v)
        relax(dag, df, paif, v)
    return v


def backward(dag: DirectGraph, Sb: set, Qb: set, db: dict, paib: dict):
    """
    向后搜索 from t
    :return:
    """
    v, minimize = extract_min(Qb, db)
    if v is not None:
        Sb.add(v)
        Qb.remove(v)
        backward_relax(dag, db, paib, v)
    return v


def backward_relax(dag: DirectGraph, db: dict, paib: dict, v: Vertex):
    """
    向后搜索过程中的 relax 取图的 weight 重量是反方向的，与 relax 不一致
    :return:
    """
    # 这里由于图是邻接链表存储的，不能够快速的反向搜索边，只能够遍历图中的所有边，可以针对图的边数据结构优化
    for x, pair in dag.edges.items():
        for y, w in pair:
            if v == y:
                if db[x] > db[v] + w:
                    # 发现更短的路径
                    db[x] = db[v] + w
                    paib[x] = v


def judge(dag: DirectGraph, df: dict, db: dict, n: Vertex):
    """
    判断是否已经找到了最短路径
    :return:
    """
    return all(df[v] + db[v] >= df[n] + db[n] for v in dag.vertexes)


def initialize(dag: DirectGraph, s: Vertex, t: Vertex):
    """
    做搜索前 forward backward 的初始化
    :return:
    """
    Sf = {s}
    Sb = {t}
    Qf = set()
    Qb = set()
    df = {s: 0}
    db = {t: 0}
    paif = {s: None}
    paib = {t: None}
    for u in dag.vertexes:
        if u != s:
            Qf.add(u)
            w = dag.get_edge_weight(s, u)
            df[u] = w
            if w < sys.maxsize:
                paif[u] = s
            else:
                paif[u] = None
        if u != t:
            Qb.add(u)
            w = dag.get_edge_weight(u, t)
            db[u] = w
            if w < sys.maxsize:
                paib[u] = t
            else:
                paib[u] = None
    return Sf, Sb, Qf, Qb, df, db, paif, paib


def print_shortest_path(paif: dict, paib: dict, n: Vertex):
    """
    输出路径
    :param n: s-->n-->t 最短路径上的顶点
    :return:
    """
    print_forward_path(paif, n)
    print(n, end='')
    print_backward_path(paib, n)


def print_forward_path(paif: dict, v: Vertex):
    """
    输出正向搜索的路径
    :param paif:
    :param v:
    :return:
    """
    if paif[v]:
        print_forward_path(paif, paif[v])
        print(paif[v], end='-->')


def print_backward_path(paib: dict, v: Vertex):
    """
    输出反向搜索的路径
    :param paib:
    :param v:
    :return:
    """
    if paib[v]:
        print('-->{}'.format(paib[v]), end='')
        print_backward_path(paib, paib[v])


def test():
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
    try:
        df, db, paif, paib, n = bi_dijkstra(dag, g, a)
        print('df: ', df)
        print('db: ', db)
        print('paif: ', paif)
        print('paib ', paib)
        print_shortest_path(paif, paib, n)
    except NoPathException as e:
        print(e)


if __name__ == '__main__':
    test()
