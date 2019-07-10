# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/7/10
@Author: Haojun Gao
@Description: 
"""

import json
import numpy as np
import pandas as pd



class DisjointSet(dict):
    """
    不相交集
    """

    def __init__(self, dict):
        pass

    def add(self, item):
        self[item] = item

    def find(self, item):
        if self[item] != item:
            self[item] = self.find(self[item])
        return self[item]

    def unionset(self, item1, item2):
        self[item2] = self[item1]


def Kruskal_1(nodes, edges):
    """
    基于不相交集实现 Kruskal 算法
    :param nodes:
    :param edges:
    :return:
    """
    forest = DisjointSet(nodes)
    MST = []
    for item in nodes:
        print(item)
        forest.add(item)
    edges = sorted(edges, key=lambda element: element[2])
    num_sides = len(nodes) - 1  # 最小生成树的边数等于顶点数减一
    for e in edges:
        node1, node2, _ = e
        parent1 = forest.find(node1)
        parent2 = forest.find(node2)
        if parent1 != parent2:
            MST.append(e)
            num_sides -= 1
            if num_sides == 0:
                return MST
            else:
                forest.unionset(parent1, parent2)
    pass


def Kruskal(nodes, edges):
    """
    Kruskal 无向图生成最小生成树
    :param nodes:
    :param edges:
    :return:
    """
    all_nodes = nodes  # set(nodes)
    used_nodes = set()
    MST = []
    edges = sorted(edges, key=lambda element: element[2], reverse=True)
    # 对所有的边按权重升序排列
    while used_nodes != all_nodes and edges:
        element = edges.pop(-1)
        if element[0] in used_nodes and element[1] in used_nodes:
            continue
        MST.append(element)
        used_nodes.update(element[:2])
        # print(used_nodes)
    return MST


def main(nodes, edges):
    print("\n\nThe undirected graph is :", edges)
    print("\n\nThe minimum spanning tree by Kruskal is : ")
    print(Kruskal_1(nodes, edges))
    print(Kruskal(nodes, edges))


if __name__ == '__main__':
    word_index_path = ".\\data\\word_index.txt"
    index_dict_path = ".\\data\\index_dict.txt"
    matrix_path = ".\\data\\mi.csv"

    mi_pd = pd.read_csv(matrix_path)
    mi_pd.drop(columns=["Unnamed: 0"], axis=1, inplace=True)
    mi_matrix = mi_pd.values

    str_file = str(word_index_path)
    with open(str_file, 'r', encoding="UTF-8") as f:
        print("Load str file from {}".format(str_file))
        str1 = f.read()
        word_index = json.loads(str1)  # 记录词的index

    str_file = str(index_dict_path)
    with open(str_file, 'r', encoding="UTF-8") as f:
        print("Load str file from {}".format(str_file))
        str1 = f.read()
        index_dict = json.loads(str1)  # 记录节点index对应的词

    nodes = set()
    for word in word_index:
        nodes.add(word)

    edges = []
    num = len(nodes)
    for i in range(num):
        if i % 100:
            print("[处理进度] {} / {}".format(i + 1, num))
        for j in range(num - i):
            k = i + j
            mi = mi_matrix[i][k]
            if mi > 0:
                print("[互信息量] {} & {} : {}".format(index_dict[str(i)], index_dict[str(k)], mi))
                edges.append((index_dict[str(i)], index_dict[str(k)], mi))


    nodes = set(list('ABCDEFGHI'))
    edges = [("A", "B", 4), ("A", "H", 8),
             ("B", "C", 8), ("B", "H", 11),
             ("C", "D", 7), ("C", "F", 4),
             ("C", "I", 2), ("D", "E", 9),
             ("D", "F", 14), ("E", "F", 10),
             ("F", "G", 2), ("G", "H", 1),
             ("G", "I", 6), ("H", "I", 7)]

    main(nodes, edges)
