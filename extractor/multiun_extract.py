#!/usr/bin/python3

#这是抽取multiun数据集的脚本

import csv
import sys
import re

source_dir = "../../en-zh.tmx"
target_dir = "../../data/corpus.csv"

t = open(target_dir,"w")
writer = csv.writer(t)

eng_re = re.compile(r'''<seg>(.+?)</seg>''',re.DOTALL)
zh_re = re.compile(r'''<seg>(.+?)</seg>''',re.DOTALL)

#限制条件
def con(eng,zh):
    esp = eng.split()
    if(len(eng)<30) or len(esp) < 7 or len(esp)>20:
        return False

    if(len(eng)<30):
        return False

    return True

def extract_line(eng,zh):
    engt = eng_re.findall(eng)[0]
    zht = zh_re.findall(zh)[0]

    if con(engt,zht):
        #print(engt)
        #print(zht)
        #print(200*"=")
        writer.writerow([engt.strip(),zht.strip()])
    

def extract():
    f = open(source_dir)

    indx = 0
    
    line = f.readline()

    while line :

        eng,zh = "",""
        
        if line.strip() == "<tu>":
            eng = f.readline()
            zh = f.readline()
            dumm = f.readline()
            
            if dumm.strip() != "</tu>":
                print("错误")
                print(eng,zh,dumm)
                sys.exit(1)

            extract_line(eng,zh)


        if indx % 1000000 == 0:
            print(indx/1000000.0,"M")
            
        indx += 1
        line = f.readline()
    

    
if __name__ == '__main__':
    print("抽取multi-un数据集")
    extract()
    
