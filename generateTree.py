# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/7/10
@Author: Haojun Gao
@Description: 
"""

import json
import numpy as np
import pandas as pd
from visualize import visualize


class DisjointSet(dict):
    """
    不相交集
    """

    def add(self, item):
        self[item] = item

    def find(self, item):
        if self[item] != item:
            self[item] = self.find(self[item])
        return self[item]

    def unionset(self, item1, item2):
        self[item2] = self[item1]


def generate_nodes_edges(word_index_path, index_dict_path, matrix_path):
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

    # nodes = set(list('ABCDEFGHI'))
    # edges = [("A", "B", 4), ("A", "H", 8),
    #          ("B", "C", 8), ("B", "H", 11),
    #          ("C", "D", 7), ("C", "F", 4),
    #          ("C", "I", 2), ("D", "E", 9),
    #          ("D", "F", 14), ("E", "F", 10),
    #          ("F", "G", 2), ("G", "H", 1),
    #          ("G", "I", 6), ("H", "I", 7)]

    return nodes, edges


def Kruskal(nodes, edges):
    """
    基于不相交集实现 Kruskal 算法
    :param nodes:
    :param edges:
    :return:
    """
    forest = DisjointSet()
    MST = []
    for item in nodes:
        print(item)
        forest.add(item)
    edges = sorted(edges, key=lambda element: element[2], reverse=True)
    print(edges)
    num_sides = len(nodes) - 1  # 最小生成树的边数等于顶点数减一
    for e in edges:
        node1, node2, _ = e
        parent1 = forest.find(node1)
        parent2 = forest.find(node2)
        print("====")
        print("{} 归属 {}".format(node1, parent1))
        print("{} 归属 {}".format(node2, parent2))
        if parent1 != parent2:
            MST.append(e)
            num_sides -= 1
            if num_sides == 0:
                return MST
            else:
                forest.unionset(parent1, parent2)
                print("{} 归属 {}".format(node1, parent2))
                print("{} 归属 {}".format(node2, parent2))
                print("====")
    pass


def maximum_spanning_tree(nodes, edges):
    print("\n\nThe undirected graph is :", edges)
    print("\n\nThe minimum spanning tree by Kruskal is : ")
    spanning_tree = Kruskal(nodes, edges)
    return spanning_tree


def generate_tree(spanning_tree, top):
    used = []
    top_tree = ["*/top"]
    temp = ["*/" + top]
    print("构建树开始")
    while len(temp) != 0:
        print(temp)
        print(top_tree)
        print("==========")
        new_temp = []
        for item in temp:
            item_list = item.split("/")
            leave = item_list[-1]
            if top == leave:
                item_list.remove(top)
            for tuple in spanning_tree:
                item_1, item_2, _ = tuple
                if item_1 in used or item_2 in used:
                    continue
                if leave == item_1:
                    new_edges = "/".join(item_list) + "/" + item_2
                    new_temp.append(new_edges)
                    top_tree.append(new_edges)
                    print(new_edges)
                elif leave == item_2:
                    new_edges = "/".join(item_list) + "/" + item_1
                    new_temp.append(new_edges)
                    top_tree.append(new_edges)
                    print(new_edges)
            used.append(leave)
        temp = new_temp

    return top_tree


def write_file(top_tree):
    with open(".\\data\\result.txt", 'w', newline='') as file:
        for edge in top_tree:
            file.write(edge + "\t\n")


if __name__ == '__main__':
    word_index_path = ".\\data\\word_index.txt"
    index_dict_path = ".\\data\\index_dict.txt"
    matrix_path = ".\\data\\mi_matrix.csv"

    # 生成边信息和节点信息
    nodes, edges = generate_nodes_edges(word_index_path, index_dict_path, matrix_path)

    # 根据边和节点生成最大生成树
    spanning_tree = maximum_spanning_tree(nodes, edges)
    print(spanning_tree)

    top = "北京"
    # 确定根节点之后生成从根节点到叶节点的路径信息
    top_tree = generate_tree(spanning_tree, top)

    # 将路径信息写进文件夹中
    write_file(top_tree)

    # 可视化生成树
    visualize(".\\data")
