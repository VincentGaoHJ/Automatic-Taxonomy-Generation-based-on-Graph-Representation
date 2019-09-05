# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/8/1
@Author: Haojun Gao
@Description: 
"""

from calcu_mi import calcu_mi
from paras import load_init_params
from generateTree import generateTree


def main(params):
    # Initialize the information of dataset.
    dataset = params['dataset']
    dataset_domain = params['dataset_domain']

    calcu_mi(dataset, dataset_domain)
    generateTree(dataset, dataset_domain)


if __name__ == '__main__':
    # params = load_init_params()
    # main(params)
    #
    # params = load_init_params("Guiyang")
    # main(params)
    #
    # params = load_init_params("Kunming")
    # main(params)
    #
    # params = load_init_params("Hangzhou")
    # main(params)
    #
    # params = load_init_params("nlp")
    # main(params)
    #
    # params = load_init_params("nlpcn")
    # main(params)
    #
    # params = load_init_params("ZhongGuoJinDaiShi")
    # main(params)

    params = load_init_params("g60763")
    main(params)