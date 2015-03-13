#!/usr/bin/python3

'''
统计信息
'''

from data import load_all
from optparse import OptionParser
import sys,logging
from nltk.corpus import stopwords
from textblob import TextBlob
import nltk
from nltk import word_tokenize as wt
from nltk.stem import WordNetLemmatizer
from matplotlib import pyplot as plt

wnl = WordNetLemmatizer()
stemmer = nltk.stem.SnowballStemmer("english")

stop = set(stopwords.words())

corpus = load_all()

def clean_words(nce):
    nce = nce.replace('’','\'')
    nce = nce.replace('‘','\'')
    words = wt(nce)
    words = set([wnl.lemmatize(word) for word in words])
    words = set([stemmer.stem(word) for word in words])
    
    return set(words)

#分析文本相关特征
def text_rel():
    #得到各个新概念文章的单词数，句子数
    for indx,nce in enumerate(corpus):
        print("第%s册有%s个句子"%(indx+1,len(nce)))

    print(50*"=")
    #得到单词个数

    words = []
    
    for indx,nce in enumerate(corpus):
        nce = ' '.join(nce)
        nce = nce.lower()
        
        twords = clean_words(nce)
        words.append(twords)
        
        if indx == 0:
            print("第%s册有%s个单词"%(indx+1,len(twords)))
        else:
            twords = twords - stop
            print("第%s册有%s个单词"%(indx+1,len(twords)))


    print(50*"=")            
    for indx,twords in enumerate(words):
        count = 0
        fuck = set()
        for i,ano in enumerate(words):
            if i == indx:
                pass
            else:
                fuck = fuck.union(ano)

        for word in twords:
            if word in fuck:
                count += 1
        
        print("第%s册有%s个相同单词"%(indx+1,count))


#分析长度特征
def length_ana():
    for indx,nce in enumerate(corpus):
        result = []
        
        for sent in nce:
            tk = wt(sent)
            result.append(len(tk))
        print(result)
        fi = int(indx/2)+1
        fig1 = plt.figure(fi)
        plt.subplot(int("21%s"%(indx%2+1)))
        plt.hist(result)
        plt.xlabel('new concept number %s'%(indx+1))
    plt.show()
    
if __name__ == '__main__':
    print(__doc__)

    parser = OptionParser()  
    parser.add_option("-t", "--task", dest="task",help="测试方法")

    (options, args) = parser.parse_args()

    if options.task == "text":
        text_rel()
    elif options.task == "length":
        length_ana()
    else:
        logging.error("方法错误")
        sys.exit(1)
