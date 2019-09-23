# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/9/23
@Author: Haojun Gao
@Description: 用来测试看关系两个节点，一个节点当成word，另一个节点极其周围节点作为topic，是否具有非对称性
"""

import os
import json
import numpy as np
import pandas as pd
from paras import load_init_params
from generateTree import generate_nodes_edges


def KL_Divergence(text_environment_order_fre, event_environment):
    """
    计算两个分布之间的KL散度值
    :param text_environment_order_fre:
    :param event_environment:
    :return:
    """

    if len(text_environment_order_fre) == len(event_environment):
        # np.core.defchararray.strip(word_environment[:,1], '()').astype(int)解释数据，将‘22’，转化为int型数据
        fre_word = text_environment_order_fre
        fre_event = np.array(event_environment)
        nil = 1 / len(text_environment_order_fre)
        P = (fre_word / np.sum(fre_word)).reshape(len(text_environment_order_fre), 1)
        Q = (fre_event / np.sum(fre_event)).reshape(len(text_environment_order_fre), 1)
        KL = np.sum(P * np.log((P + nil) / (Q + nil)))
        # KL = np.sum(Q * np.log((Q + nil) / (P + nil)))
        return KL

    else:
        return "离散分布不能对应"


def read_file(word_index_path, index_dict_path, mi_matrix_path, entity_feature_matrix_path):
    mi_pd = pd.read_csv(mi_matrix_path)
    mi_pd.drop(columns=["Unnamed: 0"], axis=1, inplace=True)
    mi_matrix = mi_pd.values

    entity_feature_pd = pd.read_csv(entity_feature_matrix_path)
    entity_feature_pd.drop(columns=["Unnamed: 0"], axis=1, inplace=True)
    entity_feature_matrix = entity_feature_pd.values

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

    return word_index, index_dict, mi_matrix, entity_feature_matrix


def create_topic(topic_id, alter_id, mi_matrix, enti_feat_matrix, index_dict):
    neighbor = set()
    n = len(mi_matrix[0])
    topic_pd = enti_feat_matrix[topic_id]
    # print("开始测试 {} 的邻居有：".format(index_dict[str(topic_id)]))
    for i in range(n):
        if i == alter_id:
            continue
        if mi_matrix[topic_id][i] > 0:
            neighbor.add(i)
            # print(index_dict[str(i)], end=",")
            topic_pd = topic_pd + enti_feat_matrix[i]
    # print()

    return topic_pd


dataset = "mafengwo"
dataset_id = "Beijing"

params = load_init_params(dataset_id)
min_kl = params['min_kl']

word_index_path = os.path.join("./data", dataset, dataset_id + "_word_index.txt")
index_dict_path = os.path.join("./data", dataset, dataset_id + "_index_dict.txt")
mi_matrix_path = os.path.join('./data', dataset, dataset_id + '_mi_matrix.csv')
kl_matrix_path = os.path.join('./data', dataset, dataset_id + '_kl_matrix.csv')
entity_feature_matrix_path = os.path.join('./data', dataset, dataset_id + '_entity_feature_matrix.csv')

# 生成边信息和节点信息
nodes, edges = generate_nodes_edges(word_index_path, index_dict_path, mi_matrix_path, kl_matrix_path)

# print(nodes)
edges = sorted(edges, key=lambda element: element[2], reverse=True)
# print(edges)

word_index, index_dict, mi_matrix, enti_feat_matrix = read_file(word_index_path, index_dict_path, mi_matrix_path,
                                                                entity_feature_matrix_path)

i = 0
for edge in edges:
    i += 1
    if i == 100:
        break
    item_1, item_2, mi, kl_1, kl_2 = edge
    print(item_1, item_2, mi)
    item_1_id = word_index[item_1]
    item_2_id = word_index[item_2]
    topic_1_pd = create_topic(item_1_id, item_2_id, mi_matrix, enti_feat_matrix, index_dict)
    topic_2_pd = create_topic(item_2_id, item_1_id, mi_matrix, enti_feat_matrix, index_dict)
    kl12 = KL_Divergence(enti_feat_matrix[item_1_id], topic_2_pd)
    kl21 = KL_Divergence(enti_feat_matrix[item_2_id], topic_1_pd)
    print("word {} word  {} : {}".format(item_1, item_2, kl_1))
    print("word {} topic {} : {}".format(item_1, item_2, kl12))
    print("word {} word  {} : {}".format(item_2, item_1, kl_2))
    print("word {} topic {} : {}".format(item_2, item_1, kl21))
    # print(kl_1, kl_2)
    # print(kl12, kl21)
