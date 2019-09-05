# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/7/10
@Author: Haojun Gao
@Description: 
"""

import os
import csv
import json
import numpy as np
import pandas as pd
from paras import load_init_params


def createUsers(data_path):
    """
    读取数据集信息
    :param data_path: 数据集路径
    :return:
        user_cut [list] 数据集
    """
    user_cut = []
    with open(data_path, encoding="utf-8") as t:
        reader = csv.reader(t)
        for sentence in reader:
            user_cut.append(sentence[0])
    return user_cut


def createWordList(keywords_path):
    """
    读取实体集合信息
    :param keywords_path: 实体集合路径
    :return:
        set_word [set] 实体集合
    """
    set_word = set()
    with open(keywords_path, 'r', encoding="utf-8") as file_to_read:
        item = file_to_read.readline()
        while item:
            set_word.add(item[:-1])
            item = file_to_read.readline()
    return set_word


def calcu_wordFrenq(sentences, keywords_set, min_tf):
    """
    统计关键词词频
    删除低频关键词
    更新关键词集合
    :param sentences: 数据集
    :param keywords_set: 关键词集合
    :return:
        word_frequency [] 实体出现词频
        keywords_set [] 更新之后的实体集合
    """
    word_frequency = {}
    temp_word = []
    total_sent = len(sentences)
    i = 0
    for sentence in sentences:
        i += 1
        if i % 1000 == 0:
            print("统计关键词词频 {} / {}".format(i, total_sent))
        word_list = sentence.split('/')
        for item in word_list:
            if item in keywords_set:
                if item not in temp_word:
                    temp_word.append(item)
                    word_frequency[item] = 1
                else:
                    word_frequency[item] += 1

    print(word_frequency)
    keywords_set = set()
    for key, value in word_frequency.items():
        if value >= min_tf:
            keywords_set.add(key)
    return word_frequency, keywords_set


def create_coocurrence_matrix(sentences, keywords_set):
    """
    创建共现次数矩阵
    :param sentences: 数据集
    :param keywords_set: 实体集合
    :return:
        coocurrence_matrix [np] 共现次数矩阵
        word_index [dictionary] 记录词的 index
        index_dict [dictionary] 记录节点 index 对应的词
    """
    coocurrence_matrix = np.zeros([len(keywords_set), len(keywords_set)])
    word_index = {}  # 记录词的index
    index_dict = {}  # 记录节点index对应的词
    for i, v in enumerate(keywords_set):
        word_index[v] = i
        index_dict[i] = v
    for sentence in sentences:
        word_list = sentence.split("/")
        intersec = keywords_set.intersection(set(word_list))
        if len(intersec) >= 2:
            temp = []
            for key_1 in intersec:
                temp.append(key_1)
                for key_2 in intersec:
                    if key_2 not in temp:
                        coocurrence_matrix[word_index[key_1]][word_index[key_2]] += 1
                        coocurrence_matrix[word_index[key_2]][word_index[key_1]] += 1

    return coocurrence_matrix, word_index, index_dict


def create_mi_matrix(keywords_set, word_frequency, coocurrence_matrix, index_dict):
    """
    计算实体互信息矩阵
    :param keywords_set: 实体集合
    :param word_frequency: 实体出现词频
    :param coocurrence_matrix: 共现次数矩阵
    :param index_dict: 记录节点 index 对应的词
    :return:
        mi_matrix [np] 实体互信息矩阵
        mi_matrix_norm [np] 实体互信息矩阵（标准化后）
    """

    total_num = 0
    for _, value in word_frequency.items():
        total_num += value

    num = len(keywords_set)
    total_coocurr = np.sum(coocurrence_matrix)
    mi_matrix = np.zeros([num, num])
    for i in range(num):
        print("[处理进度] {} / {}".format(i + 1, num))
        for j in range(num - i):
            k = i + j
            multipler = (total_num / total_coocurr) * total_num
            frequen = coocurrence_matrix[i][k] / word_frequency[index_dict[i]] * word_frequency[index_dict[k]]
            if coocurrence_matrix[i][k] != 0:
                mi = max(np.log2((multipler * frequen)), 0)
                if mi != 0:
                    print("[互信息量] {} & {} : {}".format(index_dict[i], index_dict[k], mi))

                    mi_matrix[i][k] = mi * coocurrence_matrix[i][k]
                    mi_matrix[k][i] = mi * coocurrence_matrix[k][i]

    mi_matrix_norm = np.zeros([num, num])
    for j in range(mi_matrix.shape[1]):
        sum = 0
        for i in range(mi_matrix.shape[0]):
            sum += mi_matrix[i][j]
        if sum == 0:
            print(index_dict[j])
            continue
        for i in range(mi_matrix.shape[0]):
            mi_matrix_norm[i][j] = mi_matrix[i][j] / sum
    return mi_matrix, mi_matrix_norm


def calcu_mi(dataset, dataset_id):
    """
    计算实体之间的互信息量并且保存成供下一步最小生成树的生成
    :param dataset: 数据集名称：目前包含马蜂窝（mafengwo）以及知乎（zhihu）
    :param dataset_id: 具体数据集领域名称，目前包括：
                        马蜂窝：北京（Beijing），贵阳（Guiyang），杭州（Hangzhou），昆明（Kunming）
                        知乎：中文的自然语言处理（nlpcn），中英文的自然语言处理（nlp），中国近代史（ZhongGuoJinDaiShi）
    :return: 没有返回值，只写入四个文件
    """
    # Initialize the minimum value of tf value.
    params = load_init_params(dataset_id)
    min_tf = params['min_tf']

    data_path = os.path.join("./raw_data", dataset, dataset_id + "_0.csv")
    keywords_path = os.path.join("./raw_data", dataset, dataset_id + "_geo_noun.txt")

    # 读取数据集信息
    print("读取数据集信息")
    sentences = createUsers(data_path)

    # 读取实体集合信息
    print("读取实体集合信息")
    keywords_set = createWordList(keywords_path)

    # 统计关键词词频，删除低频关键词，更新关键词集合
    print("统计关键词词频，删除低频关键词，更新关键词集合")
    word_frequency, keywords_set = calcu_wordFrenq(sentences, keywords_set, min_tf)

    # 创建共现次数矩阵
    print("创建共现次数矩阵")
    coocurrence_matrix, word_index, index_dict = create_coocurrence_matrix(sentences, keywords_set)

    # 计算实体互信息矩阵
    print("计算实体互信息矩阵")
    mi_matrix, mi_matrix_norm = create_mi_matrix(keywords_set, word_frequency, coocurrence_matrix, index_dict)

    # 保存文件
    print("保存文件")
    mi_matrix_path = os.path.join('./data', dataset, dataset_id + '_mi_matrix.csv')
    mi_pd = pd.DataFrame(mi_matrix)
    mi_pd.to_csv(mi_matrix_path)

    mi_matrix_norm_path = os.path.join('./data', dataset, dataset_id + '_mi_matrix_norm.csv')
    mi_pd = pd.DataFrame(mi_matrix_norm)
    mi_pd.to_csv(mi_matrix_norm_path)

    word_index_path = os.path.join("./data", dataset, dataset_id + "_word_index.txt")
    with open(word_index_path, "w", encoding="UTF-8") as file:
        file.writelines(json.dumps(word_index, ensure_ascii=False) + "\n")

    index_dict_path = os.path.join("./data", dataset, dataset_id + "_index_dict.txt")
    with open(index_dict_path, "w", encoding="UTF-8") as file:
        file.writelines(json.dumps(index_dict, ensure_ascii=False) + "\n")


if __name__ == '__main__':
    dataset = "tripadvisor"
    dataset_id = "g60763"
    min_tf = 50

    calcu_mi(dataset, dataset_id)
