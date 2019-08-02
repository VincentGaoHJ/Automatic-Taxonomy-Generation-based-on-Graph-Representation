# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/8/2
@Author: Haojun Gao
@Description: 
"""


def load_init_params():
    params = dict()

    # Initialize the information of dataset
    params['dataset'] = "mafengwo"
    params['dataset_domain'] = "Beijing"
    params['dataset_top_name'] = "北京"

    # Initialize the minimum value of tf value.
    params['min_tf'] = 50

    return params
