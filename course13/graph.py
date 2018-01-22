#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-01-21 10:06
# 创建图类，使用邻接链表表示图之间的边关系
import sys

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
    边的表示方式
    For a set: [('b', 1), ('c', 2)]
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def add_vertex(self, vertex: Vertex):
        """
        向图中添加新顶点
        :param vertex:
        :return:
        """
        self[vertex] = list()

    def del_vertex(self, vertex: Vertex):
        """
        图中删除某个顶点后，相应删除该顶点的信息
        :param vertex: 需要被删除的顶点
        :return:
        """
        del self[vertex]
        for k, v in self.items():
            for pair in v:
                if pair[0] == vertex:
                    v.remove(pair)
        # 因为不在图中，返回 python 能够表达的最大 int
        return sys.maxsize

    def get_edge_weight(self, x: Vertex, y: Vertex):
        """
        计算图中两个顶点的距离
        :param x:
        :param y:
        :return:
        """
        for v, weight in self[x]:
            if v == y:
                return weight
        return sys.maxsize

    @abc.abstractmethod
    def add_edge(self, x: Vertex, y: Vertex, weight=0):
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

    def add_edge(self, x: Vertex, y: Vertex, weight=0):
        """
        x-->y 有向图只需要添加一个关系
        :param x: 起始顶点
        :param y: 终结顶点
        :param weight: 权重
        :return:
        """
        self[x].append((y, weight))


class UndirectEdge(Edge):
    """
    无向图的边
    """

    def add_edge(self, x: Vertex, y: Vertex, weight=0):
        """
        ｘ--y 需要添加两个关系记录
        :param weight: 权重
        :param x:
        :param y:
        :return:
        """
        self[x].append((y, weight))
        self[y].append((x, weight))


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

    def add_edge(self, x: Vertex, y: Vertex, weight=0):
        """
        添加边关系
        :param weight: 权重
        :param x:
        :param y:
        :return:
        """
        if x not in self.vertexes or y not in self.vertexes:
            raise KeyError('图中添加的边关系必须两个顶点都在')
        self.edges.add_edge(x, y, weight)

    def get_edge_weight(self, x: Vertex, y: Vertex):
        """
        寻找图中两个顶点的权重
        :param x:
        :param y:
        :return:
        """
        return self.edges.get_edge_weight(x, y)

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
                for v, weight in self.edges[u]:
                    if v not in level:
                        # v 还没有被遍历，如果 v 已经访问过，则不做任何操作
                        level[v] = i
                        parent[v] = u
                        next_frontier.append(v)
            frontier = next_frontier
            i += 1
        return level, parent

    def DFS(self):
        """
        对图进行深度优先搜索
        :return:
        """
        parent = {}
        for s in self.vertexes:
            if s not in parent:
                # 记录 s 没有父结点
                parent[s] = None
                self.DFS_visit(s, parent)
        return parent

    def DFS_visit(self, s: Vertex, parent: dict):
        """
        从顶点 s 开始进行深度优先搜索
        :param s:
        :param parent: 用于记录 parent 关系的字典
        :return:
        """
        for u, weight in self.edges[s]:
            if u not in parent:
                # u vertex has not been visited.
                parent[u] = s
                self.DFS_visit(u, parent)

    def is_cyclic(self):
        """
        使用 DFS 判断当前图是否是循环的
        如果在使用深度优先遍历图时，遇到有边指向已经访问过的顶点，那么判断该图为有循环的；如果遍历结束都没出现前一种情况，则判断该图没有循环
        :return:
        """
        has_cycle = False
        # visited 用于记录已经被访问过的顶点，主要用于判断根顶点是否已经访问过，避免重复访问
        visited = set()
        for s in self.vertexes:
            if s not in visited:
                visited.add(s)
                this_visited = {s}
                # None 代表 s 是访问树的根结点
                if self.one_direct_visit(s, this_visited, visited):
                    has_cycle = True
                    break
        return has_cycle

    def one_direct_visit(self, s, this_visit: set, visited: set, last_visit: Vertex = None):
        """
        与 DFS_visit 的区别是传递的参数是 set 而不是 dict
        :param s: 当前正在访问的顶点
        :param this_visit: 本次深度优先搜索（单路径下）访问过的顶点，在不同路径中，this_visited 不相同
        :param visited: 记录所有已经被访问过的顶点，避免重复访问
        :param last_visit: 记录上一个访问的顶点，防止 a--b b--a 的同一条边上的循环误判
        :return:
        """
        has_cycle = False
        for u, weight in self.edges[s]:
            if u in this_visit:
                # last_visit is None 这一步是为了区分有向图和无向图
                # s == u 的判断是为了预防 a--a 自成闭环
                if last_visit is None or last_visit != u or s == u:
                    # 在本次DFS中已经访问过了 u，判断出现了循环
                    return True
            if u not in visited:
                visited.add(u)
                # 复制一个全新的 set，用于记录本次单路径访问已在本次单路径访问中访问过的
                new_visit = this_visit.copy()
                new_visit.add(u)
                if isinstance(self, UndirectGraph):
                    has_cycle = self.one_direct_visit(u, new_visit, visited, s)
                elif isinstance(self, DirectGraph):
                    has_cycle = self.one_direct_visit(u, new_visit, visited)
                if has_cycle:
                    return True
        return False

    def has_vertex(self, vertex: Vertex):
        """
        判断该顶点是否在图中
        :param vertex:
        :return:
        """
        return vertex in self.vertexes

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
    # ug.add_edge(a, a)
    ug.add_edge(a, d)
    ug.add_edge(b, c)
    ug.add_edge(c, d)
    ug.add_edge(c, e)
    ug.add_edge(c, f)
    ug.add_edge(f, g)
    print(ug)
    level, parent = ug.BFS(a)
    print('BFS:')
    print('level: ', level)
    print('parent: ', parent)
    parent = ug.DFS()
    print(parent)
    if ug.is_cyclic():
        print('发现循环')
    else:
        print('没有循环')


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
    dg.add_edge(d, a)
    dg.add_edge(b, c)
    dg.add_edge(c, d)
    dg.add_edge(c, e)
    dg.add_edge(c, f)
    dg.add_edge(g, e)
    dg.add_edge(f, g)
    print(dg)
    # level, parent = dg.BFS(a)
    # print('BFS:')
    # print('level: ', level)
    # print('parent: ', parent)
    # parent = dg.DFS()
    # print(parent)
    has_cycle = dg.is_cyclic()
    if has_cycle:
        print('发现循环')
    else:
        print('没有循环')


if __name__ == '__main__':
    test_undirect_graph()

