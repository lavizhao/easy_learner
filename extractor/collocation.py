#!/usr/bin/python3

'''
发现搭配
'''

import csv
import sys
sys.path.append("..")

from util import get_eng_common as get_eng
from util.nlp import NLP
from itertools import product
import operator
from operator import itemgetter

target_dir = "../../data/collocation.csv"
t = open(target_dir,"w")
writer = csv.writer(t)

reader = get_eng()
nlp = NLP()

p1 = ['JJ','JJR']
p2 = ['NN','NNS','NNP','NNPS']
p3 = ['IN']

ptb1 = set(product(p1,p2))
ptb2 = set(product(p2,p2))

ptt1 = set(product(p1,p1,p2))
ptt2 = set(product(p1,p2,p2))
ptt3 = set(product(p2,p1,p2))
ptt4 = set(product(p2,p2,p2))
ptt5 = set(product(p2,p3,p2))

ptt = ptt1 | ptt2 | ptt3 | ptt4 | ptt5

def bigram_pattern(c,n):
    w1,t1 = c
    w2,t2 = n

    tags = (t1,t2)

    if len(w1)<=2 or len(w2)<=2:
        return None
    
    if (t1,t2) in ptb1 or (t1,t2) in ptb2:
        return "%s %s"%(w1.lower(),w2.lower())
    else:
        return None

def trigram_pattern(c,n,nn):
    w1,t1 = c
    w2,t2 = n
    w3,t3 = nn
    tags = (t1,t2,t3)

    if len(w1)<=2 or len(w2)<=2 or len(w3)<=2:
        return None

    if tags in ptt:
        return "%s %s %s"%(w1.lower(),w2.lower(),w3.lower())
    else:
        return None
    
#用频率来找到搭配
def freq():

    #词最小出现次数
    least_freq = 100

    collocation = {}
    
    indx = 0
    for line in reader:
        
        #POS标注
        pos = nlp.tags(line)


        #返回bigram结果
        bigram = nlp.bigram(pos)
        for c,n in bigram:

            result = bigram_pattern(c,n)
            if result:
                collocation.setdefault(result,0)
                collocation[result] += 1


        trigram = nlp.trigram(pos)
        for c,n,nn in trigram:
            result = trigram_pattern(c,n,nn)
            if result:
                collocation.setdefault(result,0)
                collocation[result] += 1
        
        if indx % 10000 == 0:
            print(indx/1000000,'M',len(collocation)/1000000,'M')        
        indx += 1

    #hehe
    result = sorted(collocation.items(), key=lambda d: d[1],reverse=True)
    result = [i for i in result if i[1]>least_freq]

    for i in result:
        writer.writerow(i)
    
    
def main():
    freq()


if __name__ == '__main__':
    main()
        
