# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/7/10
@Author: Haojun Gao
@Description:
"""

import os
from graphviz import Digraph
from paras import load_init_params


def load_nodes(node_file, min_level=1, max_level=3, prefix_list=['*']):
    nodes = {'*': []}
    with open(node_file, 'r', encoding="utf-8") as f:
        for line in f:
            items = line.strip().split('\t')
            node_id = items[0]

            print(node_id)

            if node_id[-3:] == "top":
                print("==================")
                node_content = ""
                nodes["*"] = node_content
                continue

            if len(items) > 1:
                node_content = ""
            else:
                node_content = []
            nodes[node_id] = node_content

    prune_nodes = {}
    for node_id, node_content in nodes.items():
        # prune nodes
        # if not has_one_prefix(node_id, prefix_list):
        # continue
        level = len(node_id.split('/')) - 1
        if not min_level <= level <= max_level:
            continue
        # if max_level - min_level > 1 and level == min_level:
        #     node_content = []
        prune_nodes[node_id] = node_content
    return prune_nodes


def has_one_prefix(node_id, prefix_list):
    for prefix in prefix_list:
        if is_exact_prefix(node_id, prefix):
            return True
    return False


def is_exact_prefix(s, prefix):
    if not s.startswith(prefix):
        return False
    tmp = s.replace(prefix, '', 1).lstrip('/')
    if '/' in tmp:
        return False
    return True


def gen_edges(nodes):
    node_ids = list(nodes.keys())
    node_ids.sort(key=lambda x: len(x))
    edges = []
    for i in range(len(nodes) - 1):
        for j in range(i + 1, len(nodes)):
            if is_parent(node_ids[i], node_ids[j]):
                edges.append([node_ids[i], node_ids[j]])
    return edges


def is_parent(node_a, node_b):
    if not node_b.startswith(node_a):
        return False

    items_a = node_a.split('/')
    items_b = node_b.split('/')

    # 差集为1
    ret_list = [item for item in items_b if item not in items_a]
    if len(ret_list) != 1:
        return False

    if len(items_b) - len(items_a) == 1:
        return True
    else:
        return False


def gen_node_label(top_name, node_id, node_content):
    node_name = node_id.split('/')[-1]
    keywords = '\\n'.join(node_content)

    if node_id == "*":
        return '{%s}' % (top_name)

    if len(node_content) == 0:
        return node_name
    else:
        return '{%s|%s}' % (node_name, keywords)


def draw(top_name, nodes, edges, output_file):
    d = Digraph(node_attr={'shape': 'record', "fontname": "PMingLiu-CN"})
    for node_id, node_content in nodes.items():
        d.node(node_id, gen_node_label(top_name, node_id, node_content))
    for e in edges:
        d.edge(e[0], e[1])
    d.render(filename=output_file)


def main(top_name, node_file, output_file, min_level, max_level, prefix='*'):
    nodes = load_nodes(node_file, min_level, max_level, prefix)
    edges = gen_edges(nodes)
    draw(top_name, nodes, edges, output_file)


def visualize(dir, dataset_id):
    # prefix_list = ['*', '*/information_retrieval', '*/information_retrieval/web_search']

    params = load_init_params(dataset_id)
    top_name = params['dataset_top_name']

    name = ""
    result_file = os.path.join(dir, 'result' + name + '.txt')
    main(top_name, result_file, dir + "/SpanningTree" + name + "-" + dir[-14:-6] + '-our-overall-3', min_level=0,
         max_level=2)
    main(top_name, result_file, dir + "/SpanningTree" + name + "-" + dir[-14:-6] + '-our-overall-4', min_level=0,
         max_level=3)
    main(top_name, result_file, dir + "/SpanningTree" + name + "-" + dir[-14:-6] + '-our-overall-5', min_level=0,
         max_level=10)
    # main(top_name, result_file, dir + "/Computer-" + dir[-14:-6] + '-our-overall-6', min_level=0, max_level=5)
    # main(top_name, result_file, dir + "/Computer-" + dir[-14:-6] + '-our-overall-7', min_level=0, max_level=6)


if __name__ == '__main__':
    # dir = "2019-08-03-09-35-24"
    # dataset_id = "Beijing"
    # visualize(dir, dataset_id)
    #
    # dir = "2019-08-03-09-44-01"
    # dataset_id = "Guiyang"
    # visualize(dir, dataset_id)
    #
    # dir = "2019-08-03-09-44-07"
    # dataset_id = "Kunming"
    # visualize(dir, dataset_id)
    #
    # dir = "2019-08-03-09-44-36"
    # dataset_id = "Hangzhou"
    # visualize(dir, dataset_id)
    #
    # dir = "2019-08-03-10-14-17"
    # dataset_id = "nlp"
    # visualize(dir, dataset_id)
    #
    # dir = "2019-08-03-09-49-18"
    # dataset_id = "nlpcn"
    # visualize(dir, dataset_id)

    dir = "2019-09-05-12-31-21"
    dataset_id = "g60763"
    visualize(dir, dataset_id)
