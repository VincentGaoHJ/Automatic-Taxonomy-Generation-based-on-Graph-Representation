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
    params = load_init_params()
    main(params)

    params['dataset_domain'] = "Guiyang"
    params['dataset_top_name'] = "贵阳"
    params['min_tf'] = 20
    main(params)

    params['dataset_domain'] = "Kunming"
    params['dataset_top_name'] = "昆明"
    params['min_tf'] = 20
    main(params)

    params['dataset_domain'] = "Hangzhou"
    params['dataset_top_name'] = "杭州"
    params['min_tf'] = 50
    main(params)

    params['dataset'] = "zhihu"

    params['dataset_domain'] = "nlp"
    params['dataset_top_name'] = "自然语言处理"
    params['min_tf'] = 300
    main(params)

    params['dataset_domain'] = "nlpcn"
    params['dataset_top_name'] = "自然语言处理"
    params['min_tf'] = 100
    main(params)

    params['dataset_domain'] = "ZhongGuoJinDaiShi"
    params['dataset_top_name'] = "中国近代史"
    params['min_tf'] = 400
    main(params)
