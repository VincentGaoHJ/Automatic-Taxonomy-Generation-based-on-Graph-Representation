# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/8/2
@Author: Haojun Gao
@Description: 
"""


def load_init_params(dataset_domain="Beijing"):
    params = dict()

    if dataset_domain == "Beijing":
        # Initialize the information of dataset
        params['dataset'] = "mafengwo"
        params['dataset_domain'] = "Beijing"
        params['dataset_top_name'] = "北京"

        # Initialize the minimum value of tf value.
        params['min_enti_tf'] = 50
        params['min_feat_tf'] = 50

    if dataset_domain == "Guiyang":
        params['dataset'] = "mafengwo"
        params['dataset_domain'] = "Guiyang"
        params['dataset_top_name'] = "贵阳"
        params['min_enti_tf'] = 20
        params['min_feat_tf'] = 40


    if dataset_domain == "Kunming":
        params['dataset'] = "mafengwo"
        params['dataset_domain'] = "Kunming"
        params['dataset_top_name'] = "昆明"
        params['min_enti_tf'] = 20
        params['min_feat_tf'] = 40

    if dataset_domain == "Hangzhou":
        params['dataset'] = "mafengwo"
        params['dataset_domain'] = "Hangzhou"
        params['dataset_top_name'] = "杭州"
        params['min_enti_tf'] = 50
        params['min_feat_tf'] = 100

    if dataset_domain == "nlp":
        params['dataset'] = "zhihu"
        params['dataset_domain'] = "nlp"
        params['dataset_top_name'] = "NLP"
        params['min_enti_tf'] = 50
        params['min_feat_tf'] = 100

    if dataset_domain == "nlpcn":
        params['dataset'] = "zhihu"
        params['dataset_domain'] = "nlpcn"
        params['dataset_top_name'] = "自然语言处理"
        params['min_enti_tf'] = 30
        params['min_feat_tf'] = 60

    if dataset_domain == "ZhongGuoJinDaiShi":
        params['dataset'] = "zhihu"
        params['dataset_domain'] = "ZhongGuoJinDaiShi"
        params['dataset_top_name'] = "中国近代史"
        params['min_enti_tf'] = 400
        params['min_feat_tf'] = 800

    if dataset_domain == "g60763":
        params['dataset'] = "tripadvisor"
        params['dataset_domain'] = "g60763"
        params['dataset_top_name'] = "纽约"
        params['min_enti_tf'] = 200
        params['min_feat_tf'] = 400

    return params
