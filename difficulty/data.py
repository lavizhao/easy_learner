#!/usr/bin/python3

'''
载入语料，每个返回的是一个[str1,str2]的形式，str互相没有关系
'''

from nltk.corpus import stopwords
from textblob import TextBlob
import nltk
from nltk import word_tokenize as wt
from nltk.stem import WordNetLemmatizer

def clean_list(nce):
    result = []
    for line in nce:
        line = line.replace('’','\'')
        line = line.replace('‘','\'')

        result.append(line)

    return result


#载入句子，num代表册数
def load_data(num):
    num = int(num)
    f = open("../../data/nce/nce%s.txt"%(num))

    lines = f.readlines()
    lines = [i.strip() for i in lines]

    lines = clean_list(lines)
    
    return list(set(lines))

#载入全部，分别是[d1,d2,d3,d4]的形式
def load_all() :
    return [load_data(1),load_data(2),load_data(3),load_data(4)]

#返回train，label， 分别是数组的形式
import csv    
def load_train():
    f = open("../../data/nce/nce.csv")
    train,label = [],[]
    reader = csv.reader(f)

    for line in reader:
        train.append(line[0])
        label.append(int(line[1]))

    clean_list(train)
    return train,label    

def load_lda():
    f = open("../../data/nce/lda.txt")
    result = []
    for line in f:
        sp = line.split()
        sp = [float(k) for k in sp]
        result.append(sp)

    return result
    
if __name__ == '__main__':
    d = load_lda()
    print(d[0])
