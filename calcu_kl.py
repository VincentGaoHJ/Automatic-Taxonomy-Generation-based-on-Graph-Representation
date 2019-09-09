# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/9/7
@Author: Haojun Gao
@Description:
"""

import os
import csv
import json
import numpy as np
import pandas as pd
from paras import load_init_params


def create_enti_feat_matrix(sentences, keywords_set, word_index, feature_set):
    """
    创建共现次数矩阵
    :param sentences: 数据集
    :param word_index:
    :param feature_set: 特征集合
    :return:
        coocurrence_matrix [np] 共现次数矩阵
        word_index [dictionary] 记录词的 index
        index_dict [dictionary] 记录节点 index 对应的词
    """
    enti_envi_matrix = np.zeros([len(word_index), len(feature_set)])

    feat_word_index = {}  # 记录特征词的index
    feat_index_dict = {}  # 记录特征节点index对应的词

    for i, v in enumerate(feature_set):
        feat_word_index[v] = i
        feat_index_dict[i] = v

    for sentence in sentences:
        word_list = sentence.split("/")
        intersec_enti = keywords_set.intersection(set(word_list))
        intersec_feat = feature_set.intersection(set(word_list))
        if len(intersec_enti) >= 1 and len(intersec_feat) >= 1:
            for key_1 in intersec_enti:
                for key_2 in intersec_feat:
                    enti_envi_matrix[word_index[key_1]][feat_word_index[key_2]] += 1

    return enti_envi_matrix


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
        KL_1 = np.sum(P * np.log((P + nil) / (Q + nil)))
        KL_2 = np.sum(Q * np.log((Q + nil) / (P + nil)))
        return KL_1, KL_2

    else:
        return "离散分布不能对应"


def create_kl_matrix(keywords_set, enti_index_dict, enti_feat_matrix):
    """
    计算实体之间特征词分布的KL散度矩阵
    :param keywords_set: 实体集合
    :param feature_set: 特征集合
    :param enti_feat_matrix: 实体-特征矩阵
    :return:
        mi_matrix [np] 实体互信息矩阵
        mi_matrix_norm [np] 实体互信息矩阵（标准化后）
    """

    kl_value = {}
    num = len(keywords_set)
    kl_matrix = np.zeros([num, num])
    for i in range(num):
        print("[处理进度] {} / {}".format(i + 1, num))
        for j in range(num - i - 1):
            k = i + j + 1
            kl_1, kl_2 = KL_Divergence(enti_feat_matrix[i], enti_feat_matrix[k])
            print("[KL散度矩阵] {} & {} : {} {}".format(enti_index_dict[i], enti_index_dict[k], kl_1, kl_2))
            kl_matrix[i][k] = kl_1
            kl_matrix[k][i] = kl_2
            kl_value[str((enti_index_dict[i], enti_index_dict[k]))] = str(kl_1) + str(kl_2)

    kl_value_sort = sorted(kl_value.items(), key=lambda x: x[1])

    return kl_matrix, kl_value, kl_value_sort
