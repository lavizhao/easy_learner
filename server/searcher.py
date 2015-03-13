#!/usr/bin/python
#coding: utf-8

#查询函数

import lucene

import sys
sys.path.append("..")
import util
from util.rake import Rake

print("load vm")
index_dir = '../../data/index/'

#搭配地址
location_dir = '../../data/location/'

lucene.initVM()

directory = lucene.SimpleFSDirectory(lucene.File(index_dir))
analyzer = lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT)

directory1 = lucene.SimpleFSDirectory(lucene.File(location_dir))
analyzer1 = lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT)


rake = Rake("../../data/SmartStoplist.txt")


def search(word):
    print("searching ")
    
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    
    searcher = lucene.IndexSearcher(directory,True)
    query = lucene.QueryParser(lucene.Version.LUCENE_CURRENT,'eng',analyzer).parse(word)
    #print "查询"
    results = searcher.search(query,None,20)
    score_docs = results.scoreDocs

    fuck = []
    
    for score_doc in score_docs:
        doc = searcher.doc(score_doc.doc)

        p = (doc['eng'],doc['zh'])

        fuck.append(p)
        
    searcher.close()
    return fuck

def search_location(word):
    print("searching ")
    
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    
    searcher = lucene.IndexSearcher(directory1,True)
    query = lucene.QueryParser(lucene.Version.LUCENE_CURRENT,'eng',analyzer1).parse(word)
    #print "查询"
    results = searcher.search(query,None,20)
    score_docs = results.scoreDocs

    fuck = []
    
    for score_doc in score_docs:
        doc = searcher.doc(score_doc.doc)

        p = doc['eng']

        fuck.append(p)
        
    searcher.close()
    return fuck

def get_location_text(result):
    return ' | '.join(result)

    
def get_text(result):
    rs = u""
    for number,line in enumerate(result):
        keywords = rake.run(line[0])
        keywords = [i for i,j in keywords if len(i) > 3]
        keywords = ' | '.join(keywords)
        rs += u'''<p> 例句%s </p><p>英语 %s</p> <p>汉语 %s </p> \n 
        <div class=\"well\">
        <p>关键词: %s</p>
        </div>
        <hr/>\n
        '''%(number+1,line[0],line[1],keywords)

    return rs
    
if __name__ == '__main__':
    rt = search("india")
    for ans in rt:
        print "英语",ans[0]
        print "汉语",ans[1]
        print 50*"="

    
    
