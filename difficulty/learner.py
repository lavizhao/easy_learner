#!/usr/bin/python3
#coding: utf-8


'''
作用，训练并交叉验证，四类特征分别为 1.词（word）；2.长度（length）；3.结构（struct）；4.主题（topic），主题可能后来会有较大变化，执行的时候-f word即可，全选是all

'''

from scipy import sparse

from data import load_train,load_lda
from nltk import word_tokenize as wt
from textblob import TextBlob

import numpy as np
from sklearn import cross_validation

#classfier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB as NB
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.ensemble import GradientBoostingClassifier as GBDT
from sklearn.linear_model import LinearRegression as LReg

from sklearn.decomposition import TruncatedSVD as SVD

#tf-idf
from sklearn.feature_extraction.text import TfidfVectorizer

Feature = ["word","length","struct","lsa","lda"]

from optparse import OptionParser
import logging,sys

sentences,label = load_train()
lda_info = load_lda()

#得到tfidf
def get_tfidf(model_name):
    vectorizer = TfidfVectorizer(max_features=None,min_df=4,max_df=1.0,sublinear_tf=True,ngram_range=(1,2),smooth_idf=True,token_pattern=r'\w{1,}',analyzer='word',strip_accents='unicode')
    train = vectorizer.fit_transform(sentences)

    if model_name not in ["lr","knn"]:
        return train.toarray()

    return train

tags = ['WDT', 'RBS', 'RB', 'DT', 'NNP', 'WP', 'JJS', 'NNPS', 'TO', 'PRP', 'PRP$', 'VBN', 'VBP', 'VBZ', 'MD', 'UH', 'CD', 'CC', 'SYM', 'JJR', 'RBR', 'JJ', 'POS', 'WRB', 'VBD', 'IN', 'VB', 'VBG', 'WP$', 'NNS', 'NN', 'FW', 'EX']
def match_tag(sent):
    result = []
    for tag in tags:
        result.append(sent.count(tag))

    return result

    
#得到长度数据
def get_length():
    train = []
    for sent in sentences:
        #字符长度
        a1 = len(sent)

        #单词个数
        a2 = len(wt(sent))

        #'s个数，也就是所有格个数
        a3 = sent.count('\'s')

        #标点符号的个数 比如.和？
        a4 = sent.count('.') + sent.count('?')

        #最长单词长度
        b = wt(sent)
        a5 = len(max(b))

        train.append([a1,a2,a3,a4,a5])

    return train

def get_structure():
    train = []
    for sent in sentences:
        blob = TextBlob(sent)

        #名词短语个数
        a1 = len(blob.noun_phrases)

        #词性个数
        af = blob.tags
        af = [j for (i,j) in af ]

        #parse
        a2 = blob.parse().count('O')

        temp = [a1,a2]
        temp.extend(match_tag(af))
        
        train.append(temp)

    return train

def get_lsa():
    print("lsa")    
    train = get_tfidf("lr")
    lsa = SVD(n_components=400)
    train = lsa.fit_transform(train)

    return train
    
def get_model(model_name,feature):
    clf = " "
    if model_name == "lr" :
        if feature == "word":
            clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=1,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.1)
        elif feature == "length":
            clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=0.09,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.1)
        elif feature == "struct":
            clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=2,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.1)
        elif feature == "lsa":
            clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=2,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.1)
        else:
            sp = feature.split(',')
            if set(sp) == set(["word","length","struct"]):
                clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=1,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.2)
            elif set(sp) == set(["word","length","lsa"]):
                clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=0.8,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.2)
            elif set(sp) == set(["struct","length","lsa"]):
                clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=2,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.3)
            elif set(sp) == set(["struct","length","lsa","word"]):
                clf = LogisticRegression(penalty='l2',dual=False,fit_intercept=True,C=3,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=2)
            
                
            elif "word" in sp  and "length" in sp:
                clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=0.2,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.2)
            elif "word" in sp and "struct" in sp:
                clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=5,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.2)
            elif "word" in sp and "lsa" in sp:
                clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=2,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.2)
            elif "length" in sp and "struct" in sp:
                clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=0.08,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.2)
            elif "length" in sp and "lsa" in sp:
                clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=0.3,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.2)
            elif "struct" in sp and "lsa" in sp:
                clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=2.5,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.2)
            else:
                clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=True,C=0.09,tol=0.0001,class_weight=None, random_state=None, intercept_scaling=0.1)
                
    elif model_name == "nb":
        clf = NB()
    elif model_name == "knn":
        if feature == "lsa":
            clf = KNN(n_neighbors=60)
        else:
            clf = KNN(n_neighbors=120)
        
    elif model_name == "rf":
        clf = RF(n_estimators=1000,max_features="auto",max_depth=8,min_samples_split=10,min_samples_leaf=2)
        
    elif model_name == "gbdt":
        clf = GBDT(n_estimators=400,max_features="auto",max_depth=8,min_samples_split=10,min_samples_leaf=2)
        
    elif model_name == "svm":
        if feature == "word" or feature == "length":
            clf = svm.SVC(C=0.8,kernel='rbf',gamma=0.08)
        elif feature == "structure":
            clf = svm.SVC(C=0.1,kernel='rbf',gamma=0.08)
        else:
            sp = feature.split(',')
            if "struct" in sp and "lsa" in sp:
                clf = svm.SVC(C=0.9,kernel='rbf',gamma=0.08)
            else:
                clf = svm.SVC(C=3,kernel='rbf',gamma=0.08)
    else:
        print("你只能从LR,NB,RF几种模型里选择")
        sys.exit(1)
    return clf
    
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-m", "--model", dest="model", \
                      help=u"选择模型:可选择的有LR，RF，NB", metavar="your_model",default="LR")

    parser.add_option("-f","--feature",dest="feature",help="特征选择")

    (options, args) = parser.parse_args()
    
    feature = options.feature

    train = ""
    if feature == "word":
        train = get_tfidf(options.model)
    elif feature == "length":
        train = get_length()
        train = np.array(train)
    elif feature == "struct":
        train = get_structure()
        train = np.array(train)
    elif feature == "lsa":
        train = get_lsa()
    elif feature == "lda":
        train = lda_info
        train = np.array(train)
    elif ',' in feature:
        sp = feature.split(',')
        print(sp)
        train = ""
        for indx,f in enumerate(sp):
            temp = ""
            if f == "word":
                temp = get_tfidf(options.model)
                if options.model == "lr"  or options.model == "knn":
                    temp = temp.toarray()
                    
            elif f == "length":
                temp = get_length()
                temp = np.array(temp)
            elif f == "struct":
                temp = get_structure()
                temp = np.array(temp)
            elif f == "lsa":
                temp = get_lsa()
                temp = np.array(temp)
            else:
                logging.error("方法没有见过%s"%(f))
                sys.exit(1)

            if indx == 0:
                train = temp
            else:
                train = np.hstack((train,temp))
                
    else:
        sys.exit(1)
        

    print("训练数据维度",train.shape)
    model = get_model(options.model,options.feature)

    print("交叉验证")
    #cv = cross_validation.cross_val_score(model,train,label,cv=20,scoring='f1',n_jobs=3)
    cv = cross_validation.cross_val_score(model,train,label,cv=20,scoring='accuracy',n_jobs=3)

    print("cv score:",cv)
    print("cv mean:",np.mean(cv))

    
