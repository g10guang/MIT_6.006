#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-01-21 10:06
# 创建图类，使用邻接链表表示图之间的边关系

from course8.abchash import obj2int
import abc


class Vertex(object):
    """
    用于表示图的顶点
    """

    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

    def __hash__(self) -> int:
        try:
            return hash(self.value)
        except TypeError:
            # self.value 不能够计算 hash，通过 Pickle 将其转化为 十六进制，然后将其转化为 int
            return obj2int(self.value)

    def __repr__(self) -> str:
        return repr(self.value)


class Edge(dict, abc.ABC):
    """
    用于表示图的边
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def add_vertex(self, vertex: Vertex):
        """
        向图中添加新顶点
        :param vertex:
        :return:
        """
        self[vertex] = set()

    def del_vertex(self, vertex: Vertex):
        """
        图中删除某个顶点后，相应删除该顶点的信息
        :param vertex: 需要被删除的顶点
        :return:
        """
        del self[vertex]
        for k, v in self.items():
            if vertex in v:
                v.remove(vertex)

    @abc.abstractmethod
    def add_edge(self, x: Vertex, y: Vertex):
        """
        添加边关系
        :return:
        """

    def __repr__(self) -> str:
        l = []
        for k, v in self.items():
            msg = 'vertex: {} adj list: {}'.format(k, v)
            l.append(msg)
        return '\n'.join(l)


class DirectEdge(Edge):
    """
    有向图的边
    """

    def add_edge(self, x: Vertex, y: Vertex):
        """
        x-->y 有向图只需要添加一个关系
        :param x: 起始顶点
        :param y: 终结顶点
        :return:
        """
        self[x].add(y)


class UndirectEdge(Edge):
    """
    无向图的边
    """

    def add_edge(self, x: Vertex, y: Vertex):
        """
        ｘ--y 需要添加两个关系记录
        :param x:
        :param y:
        :return:
        """
        self[x].add(y)
        self[y].add(x)


class Graph(abc.ABC):
    """
    使用邻接链表来记录顶点之间的边关系
    """

    def __init__(self) -> None:
        super().__init__()
        self.vertexes = set()
        self.edges = self.init_edge()

    @abc.abstractmethod
    def init_edge(self) -> Edge:
        """
        初始化边
        这一步是为了兼容有向图和无向图的区别，在本代码中有向图和无向图的区别就是 Edge 不一样而已
        :return:
        """
        pass

    def add_vertex(self, vertex: Vertex):
        """
        向图中添加一个顶点
        :param vertex:
        :return:
        """
        if vertex in self.vertexes:
            raise Exception('重复添加顶点')
        self.vertexes.add(vertex)
        self.edges.add_vertex(vertex)

    def del_vertex(self, vertex: Vertex):
        """
        在图中删除一个顶点
        :param vertex:
        :return:
        """
        self.vertexes.remove(vertex)
        self.edges.del_vertex(vertex)

    def add_edge(self, x: Vertex, y: Vertex):
        """
        添加边关系
        :param x:
        :param y:
        :return:
        """
        if x not in self.vertexes or y not in self.vertexes:
            raise KeyError('图中添加的边关系必须两个顶点都在')
        self.edges.add_edge(x, y)

    def BFS(self, s):
        """
        使用深度优先方法遍历该图
        :param s: 为开始遍历的顶点
        :return:
        返回每个顶点是在第几层遍历的 level，以及每个顶点的在遍历过程中的上级顶点
        """
        if s not in self.vertexes:
            # 顶点不存在于图中
            raise KeyError('顶点 {} 不在图中'.format(s))
        level = {s: 0}      # 用于记录每个顶点是在第几层遍历的
        parent = {s: None}  # 记录每个顶点在ＢＳＦ中谁是它的父顶点，因为ＢＦＳ遍历最后会得到一棵以　ｓ　为根结点的树
        frontier = [s]      # 记录上一层的遍历结果
        i = 1               # 记录正在遍历的是第几层
        while frontier:
            next_frontier = []       # 用于暂存 frontier 结果
            for u in frontier:
                for v in self.edges[u]:
                    if v not in level:
                        # v 还没有被遍历，如果 v 已经访问过，则不做任何操作
                        level[v] = i
                        parent[v] = u
                        next_frontier.append(v)
            frontier = next_frontier
            i += 1
        return level, parent

    def __repr__(self) -> str:
        v = [repr(x) for x in self.vertexes]
        return '顶点：{}\n边：\n{}'.format(' '.join(v), repr(self.edges))


class DirectGraph(Graph):
    """
    有向图
    """

    def init_edge(self) -> Edge:
        return DirectEdge()


class UndirectGraph(Graph):
    """
    无向图
    """

    def init_edge(self) -> Edge:
        return UndirectEdge()


def test_undirect_graph():
    """
    测试无向图
    :return:
    """
    ug = UndirectGraph()
    a = Vertex('a')
    b = Vertex('b')
    c = Vertex('c')
    d = Vertex('d')
    e = Vertex('e')
    f = Vertex('f')
    g = Vertex('g')
    ug.add_vertex(a)
    ug.add_vertex(b)
    ug.add_vertex(c)
    ug.add_vertex(d)
    ug.add_vertex(e)
    ug.add_vertex(f)
    ug.add_vertex(g)
    ug.add_edge(a, b)
    ug.add_edge(a, d)
    ug.add_edge(b, c)
    ug.add_edge(c, d)
    ug.add_edge(c, e)
    ug.add_edge(c, f)
    ug.add_edge(f, g)
    level, parent = ug.BFS(a)
    print(ug)
    print('BFS:')
    print('level: ', level)
    print('parent: ', parent)


def test_direct_graph():
    """
    测试有向图
    :return:
    """
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
    dg.add_edge(a, b)
    dg.add_edge(a, d)
    dg.add_edge(b, c)
    dg.add_edge(c, d)
    dg.add_edge(c, e)
    dg.add_edge(c, f)
    dg.add_edge(g, e)
    dg.add_edge(f, g)
    print(dg)
    level, parent = dg.BFS(a)
    print('BFS:')
    print('level: ', level)
    print('parent: ', parent)


if __name__ == '__main__':
    test_direct_graph()

