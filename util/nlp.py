'''
一些常用的nlp函数
'''

from textblob import TextBlob as tb

class NLP:
    def __init__(self):
        pass

    def tags(self,sentence):
        blob = tb(sentence)
        return blob.tags

    #list的bigram和trigram
    def bigram(self,s):
        for i in range(len(s)-1):
            c,n = s[i],s[i+1]
            yield [c,n]

    def trigram(self,s):
        for i in range(len(s)-2):
            c,n,nn = s[i],s[i+1],s[i+2]
            yield [c,n,nn]
