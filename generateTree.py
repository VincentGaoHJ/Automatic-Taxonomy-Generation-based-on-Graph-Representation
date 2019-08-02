# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/7/10
@Author: Haojun Gao
@Description: 
"""

import os
import csv
import json
import shutil
import datetime
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


def create_dir():
    """
    为本次实验创建一个独立的文件夹
    把 data 文件夹中的初始文件拷贝到单独文件夹中
    :return:
    """
    root = os.getcwd()
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    folder = os.path.join(root, nowTime)
    # 创建文件夹
    os.makedirs(folder)

    return folder


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


def Kruskal(nodes, edges, data_path):
    """
    基于不相交集实现 Kruskal 算法
    :param nodes:
    :param edges:
    :return:
    """
    confi_flag = 1

    sentences = createUsers(data_path)

    forest = DisjointSet()
    MST = []
    for item in nodes:
        print(item)
        forest.add(item)
    edges = sorted(edges, key=lambda element: element[2], reverse=True)
    print(edges)
    num_sides = len(nodes) - 1  # 最小生成树的边数等于顶点数减一
    circum_max = {}
    for e in edges:
        node1, node2, _ = e
        parent1 = forest.find(node1)
        parent2 = forest.find(node2)
        # print("====")
        # print("{} 归属 {}".format(node1, parent1))
        # print("{} 归属 {}".format(node2, parent2))
        if parent1 == parent2:
            if confi_flag == 0:
                pass
            else:
                copy_tree = find_circum(MST, node1, node2)
                # print(copy_tree)
                for tuple in copy_tree:
                    if tuple in circum_max:
                        circum_max[tuple] += 1
                    else:
                        circum_max[tuple] = 1

                cut_line = find_cut_line(copy_tree, sentences)
                if cut_line[1] != 0:
                    if cut_line[0][0] == node1 and cut_line[0][1] == node2:
                        pass
                        # print("环路出现暨删除 {} & {} ".format(node1, node2))
                    else:
                        # pass
                        print("删除的环路 {} & {}".format(cut_line[0][0], cut_line[0][1]))
                        print("添加的环路 {} & {} ".format(node1, node2))
                        print("======================================")
                        MST.remove(cut_line[0])
                        MST.append(e)
                    # raise Exception

        else:
            MST.append(e)
            num_sides -= 1
            if num_sides == 0:
                return MST
            else:
                forest.unionset(parent1, parent2)
                # print("{} 归属 {}".format(parent2, parent1))
                # print("====")
    pass


def createUsers(data_path):
    user_cut = []
    with open(data_path) as t:
        reader = csv.reader(t)
        for sentence in reader:
            word_set = set(sentence[0].split('/'))
            user_cut.append(word_set)
    return user_cut


def find_cut_line(tree, sentences):
    spot_all = set()
    confi_result = {}
    for tuple in tree:
        spot_1, spot_2, _ = tuple
        spot_all.add(spot_1)
        spot_all.add(spot_2)
    for tuple in tree:
        spot_1, spot_2, _ = tuple
        spot_target = {spot_1, spot_2}
        spot_circum = spot_all.difference(spot_target)
        confi = calcu_confidence(spot_target, spot_circum, sentences)
        confi_result[tuple] = confi

    confi_sorted = sorted(confi_result.items(), key=lambda x: x[1], reverse=True)

    return confi_sorted[0]


def calcu_confidence(spot_target, spot_circum, sentences):
    total_tar = 0
    total_cir = 0
    for word_set in sentences:
        tar_num = word_set.intersection(spot_target)
        if len(tar_num) == 2:
            total_tar += 1
            cir_num = word_set.intersection(spot_circum)
            if len(cir_num) == len(spot_circum):
                total_cir += 1
    # print("{} 的置信度统计之目标置信度值：{}".format(spot_target, total_cir / total_tar))

    confidence = total_cir / total_tar
    print("{} 的置信度统计之目标置信度值：{}".format(spot_target, confidence))

    return confidence


def maximum_spanning_tree(nodes, edges, data_path):
    print("\n\nThe undirected graph is :", edges)
    print("\n\nThe minimum spanning tree by Kruskal is : ")
    spanning_tree = Kruskal(nodes, edges, data_path)
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


def write_file(top_tree, folder):
    path = os.path.join(folder, "result.txt")
    with open(path, 'w', newline='') as file:
        for edge in top_tree:
            file.write(edge + "\t\n")


def find_circum(MST, key_1, key_2):
    copy_tree = MST[:]
    copy_tree.append((key_1, key_2, 1))
    flag = 1
    wait_delete_key = []
    while flag == 1:
        circum_dict = {}
        for tuple in copy_tree:
            item_1, item_2, _ = tuple
            # print(item_2)
            # print(item_1)
            if item_1 in wait_delete_key or item_2 in wait_delete_key:
                continue
            if item_1 in circum_dict:
                circum_dict[item_1] += 1
            else:
                circum_dict[item_1] = 1

            if item_2 in circum_dict:
                circum_dict[item_2] += 1
            else:
                circum_dict[item_2] = 1
        flag = 0
        for key, value in circum_dict.items():
            if value == 1:
                flag = 1
                # print("删除节点", key)
                wait_delete_key.append(key)

    final_tree = []
    for tuple in copy_tree:
        item_1, item_2, _ = tuple
        if item_1 in wait_delete_key or item_2 in wait_delete_key:
            continue
        final_tree.append(tuple)
    # raise Exception
    return final_tree


def generateTree(dataset, dataset_id, top):
    data_path = os.path.join(".\\raw_data", dataset, dataset_id + "_0.csv")
    word_index_path = os.path.join(".\\data", dataset, dataset_id + "_word_index.txt")
    index_dict_path = os.path.join(".\\data", dataset, dataset_id + "_index_dict.txt")
    matrix_path = os.path.join('.\\data', dataset, dataset_id + '_mi_matrix.csv')

    folder = create_dir()

    # 生成边信息和节点信息
    nodes, edges = generate_nodes_edges(word_index_path, index_dict_path, matrix_path)

    # 根据边和节点生成最大生成树
    spanning_tree = maximum_spanning_tree(nodes, edges, data_path)
    print(spanning_tree)

    # 确定根节点之后生成从根节点到叶节点的路径信息
    top_tree = generate_tree(spanning_tree, top)

    # 将路径信息写进文件夹中
    write_file(top_tree, folder)

    # 可视化生成树
    visualize(folder)


if __name__ == '__main__':
    dataset = "mafengwo"
    dataset_id = "Beijing"
    dataset_top = "北京"

    generateTree(dataset, dataset_id, dataset_top)
