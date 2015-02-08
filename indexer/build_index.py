#!/usr/bin/python
#coding: utf-8

#建索引的文件

import lucene
import csv

index_dir = '../../data/index/'
data_dir = '../../data/corpus.csv'

lucene.initVM()
directory = lucene.SimpleFSDirectory(lucene.File(index_dir))
analyzer = lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT)

def build_index():
    f = open(data_dir)
    reader = csv.reader(f)

    print("开始创建索引")

    indx = 0

    writer = lucene.IndexWriter(directory,analyzer,True, lucene.IndexWriter.MaxFieldLength.UNLIMITED)

    for line in reader:
        eng,zh = line[0],line[1]

        doc = lucene.Document()
        
        doc.add(lucene.Field('eng',eng,lucene.Field.Store.YES, lucene.Field.Index.ANALYZED))
        doc.add(lucene.Field('zh',zh,lucene.Field.Store.YES, lucene.Field.Index.NOT_ANALYZED))

        writer.addDocument(doc)
        
        if indx % 100000 == 0:
            print("%sK"%(indx/1000))
            
        indx += 1

    print("写引擎优化")
    writer.optimize()
    writer.close()

if __name__ == '__main__':
    build_index()

