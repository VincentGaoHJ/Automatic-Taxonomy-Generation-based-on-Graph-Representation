# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/7/9
@Author: Haojun Gao
@Description: 
"""

import csv
import json
import numpy as np
import pandas as pd


class TextRank(object):

    def __init__(self, word_index_path, index_dict_path, matrix_path, window, alpha, iternum):
        self.word_index_path = word_index_path
        self.index_dict_path = index_dict_path
        self.matrix_path = matrix_path
        self.window = window
        self.alpha = alpha
        self.iternum = iternum  # 迭代次数

    def createUsers(self, data_path):
        user_cut = []
        with open(data_path) as t:
            reader = csv.reader(t)
            for sentence in reader:
                user_cut.append(sentence[0])
        return user_cut

    # 对句子进行分词
    def createWordList(self, keywords_path):
        set_word = set()
        with open(keywords_path, 'r') as file_to_read:
            item = file_to_read.readline()
            while item:
                set_word.add(item[:-1])
                item = file_to_read.readline()
        return set_word

    # 根据边的相连关系，构建矩阵
    def createMatrix(self):

        mi_pd = pd.read_csv(self.matrix_path)
        mi_pd.drop(columns=["Unnamed: 0"], axis=1, inplace=True)
        self.matrix = mi_pd.values

        str_file = str(self.word_index_path)
        with open(str_file, 'r', encoding="UTF-8") as f:
            print("Load str file from {}".format(str_file))
            str1 = f.read()
            self.word_index = json.loads(str1)  # 记录词的index

        str_file = str(self.index_dict_path)
        with open(str_file, 'r', encoding="UTF-8") as f:
            print("Load str file from {}".format(str_file))
            str1 = f.read()
            self.index_dict = json.loads(str1)  # 记录节点index对应的词

    # 根据textrank公式计算权重
    def calPR(self):
        self.word_set = set()
        for word in self.word_index:
            self.word_set.add(word)
        self.PR = np.ones([len(set(self.word_set)), 1])
        for i in range(self.iternum):
            self.PR = (1 - self.alpha) + self.alpha * np.dot(self.matrix, self.PR)

    # 输出词和相应的权重
    def printResult(self):
        word_pr = {}
        for i in range(len(self.PR)):
            word_pr[self.index_dict[str(i)]] = self.PR[i][0]
        res = sorted(word_pr.items(), key=lambda x: x[1], reverse=True)

        return res


if __name__ == '__main__':
    word_index_path = ".\\data\\word_index.txt"
    index_dict_path = ".\\data\\index_dict.txt"
    matrix_path = ".\\data\\mi.csv"
    tr = TextRank(word_index_path, index_dict_path, matrix_path, 3, 0.85, 700)  # 创建对象
    tr.createMatrix()
    tr.calPR()
    results = tr.printResult()
    print(results)
