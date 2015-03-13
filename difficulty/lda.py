#!/usr/bin/python3

'''
抽取lda
'''

from nltk.corpus import stopwords
from textblob import TextBlob
import nltk
from nltk import word_tokenize as wt
from nltk.stem import WordNetLemmatizer

from gensim import corpora, models, similarities
from gensim.models import LdaModel

stop = set(stopwords.words())

from data import load_train

sentences,label = load_train()

texts = [[word for word in document.lower().split() if word not in stop] for document in sentences]

dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]

topic_num = 100

lda = LdaModel(corpus, num_topics=topic_num,eval_every=5,passes=200)  # train model

max_num = topic_num + 10

if __name__ == '__main__':
    target = open("../../data/nce/lda.txt","w")
    for i in corpus:
        info = lda[i]
        t = [0 for k in range(max_num)]
        #tp 是主题数 p是概率
        for tp,p in info:
            t[tp] = p

        t = [str(j) for j in t]
        t = ' '.join(t)
        target.write(t+"\n")


