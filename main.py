# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/8/1
@Author: Haojun Gao
@Description: 
"""

from calcu_mi import calcu_mi
from generateTree import generateTree

if __name__ == '__main__':
    dataset = "zhihu"
    dataset_id = "nlp"
    dataset_top = "自然语言处理"
    min_tf = 120

    calcu_mi(dataset, dataset_id, min_tf)
    generateTree(dataset, dataset_id, dataset_top)