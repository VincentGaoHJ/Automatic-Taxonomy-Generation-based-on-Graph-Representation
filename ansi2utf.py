# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/8/2
@Author: Haojun Gao
@Description: 
"""

# ANSI文件转UTF-8
import codecs
import os

def ansi2utf(path):
    files = os.listdir(file_path)

    for file in files:
        print(file)
        file_name = file_path + '\\' + file
        try:
            f = codecs.open(file_name, 'r', 'ansi')
            ff = f.read()
        except:
            f = codecs.open(file_name, 'r', 'utf-8')
            ff = f.read()

        file_object = codecs.open(file_path + '\\' + file, 'w', 'utf-8')
        file_object.write(ff)

# 文件所在目录
# file_path = ".\\raw_data\\mafengwo"
# ansi2utf(file_path)
# file_path = ".\\raw_data\\zhihu"
# ansi2utf(file_path)
file_path = ".\\raw_data\\tripadvisor"
ansi2utf(file_path)

