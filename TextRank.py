# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/7/9
@Author: Haojun Gao
@Description: 
"""

import csv
import numpy as np
import math
import jieba
import jieba.posseg as pseg


class TextRank(object):

    def __init__(self, data_path, keywords_path, window, alpha, iternum):
        self.sentences = self.createUsers(data_path)
        self.word_set = self.createWordList(keywords_path)
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
        self.matrix = np.zeros([len(set(self.word_set)), len(set(self.word_set))])
        self.word_index = {}  # 记录词的index
        self.index_dict = {}  # 记录节点index对应的词

        for i, v in enumerate(set(self.word_set)):
            self.word_index[v] = i
            self.index_dict[i] = v
        temp_set = []
        for key_1 in self.word_set:
            temp_set.append(key_1)
            for key_2 in self.word_set:
                if key_2 in temp_set:
                    continue
                mi = self.caicu_mi(key_1, key_2)
                self.matrix[self.word_index[key_1]][self.word_index[key_2]] = mi
                self.matrix[self.word_index[key_2]][self.word_index[key_1]] = mi
                # 归一化
        for j in range(self.matrix.shape[1]):
            sum = 0
            for i in range(self.matrix.shape[0]):
                sum += self.matrix[i][j]
            for i in range(self.matrix.shape[0]):
                self.matrix[i][j] /= sum

    # 根据textrank公式计算权重
    def calPR(self):
        self.PR = np.ones([len(set(self.word_set)), 1])
        for i in range(self.iternum):
            self.PR = (1 - self.alpha) + self.alpha * np.dot(self.matrix, self.PR)

    # 输出词和相应的权重
    def printResult(self):
        word_pr = {}
        for i in range(len(self.PR)):
            word_pr[self.index_dict[i]] = self.PR[i][0]
        res = sorted(word_pr.items(), key=lambda x: x[1], reverse=True)
        print(res)

    def caicu_mi(self, item_1, item_2):
        num_poi = 0
        num_item = 0
        both = 0
        for sentence in self.sentences:
            if item_1 in sentence:
                num_item += 1
            if item_2 in sentence:
                num_poi += 1
            if item_1 in sentence and item_2 in sentence:
                both += 1
        total = len(self.sentences)

        mutual_information = 0
        if both == 0:
            # print("{} 与 {} 互信息量 {}".format(item_1, item_2, mutual_information))
            return mutual_information

        mutual_information = total * both / (num_poi * num_item)
        mutual_information = math.log2(mutual_information)

        if mutual_information < 0:
            mutual_information = 0
            # print("{} 与 {} 互信息量 {}".format(item_1, item_2, mutual_information))
            return mutual_information

        mutual_information *= both
        print("{} 与 {} 互信息量 {}".format(item_1, item_2, mutual_information))
        return mutual_information


if __name__ == '__main__':
    # s = '程序员(英文Programmer)是从事程序开发、维护的专业人员。一般将程序员分为程序设计人员和程序编码人员，但两者的界限并不非常清楚，特别是在中国。软件从业人员分为初级程序员、高级程序员、系统分析员和项目经理四大类。'
    data_path = ".\\data\\0.csv"
    keywords_path = ".\\data\\geo_noun.txt"
    # keywords_path = ".\\data\\keywords.txt"
    tr = TextRank(data_path, keywords_path, 3, 0.85, 700)  # 创建对象
    tr.createMatrix()
    tr.calPR()
    tr.printResult()
