#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-01-22 19:59
# 如果在图中需要搜索的目标是 single-source s and single-target t，那么可以对 Dijkstra 算法进行优化
# 从 s 开始进行 forward Dijkstra search；从 t 开始进行 backward Dijkstra search
# Qf df 分别表示 forward search 中尚未确定的顶点、df 表示当前其他结点到 s 的距离
# Qb db 分别表示 backward search 中尚未确定的顶点、db 表示当前其他结点到 t 的最短路径
