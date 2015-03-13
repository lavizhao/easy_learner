#coding: utf-8
'''
一些常用函数
'''

import csv

data_dir = '../../data/corpus.csv'
data_dir1 = '../../data/corpus_common.csv'

def get_eng():
    f = open(data_dir)
    reader = csv.reader(f)

    for line in reader:
        yield line[0]

def get_eng_common():
    f = open(data_dir1)
    reader = csv.reader(f)

    for line in reader:
        yield line[0]
