#!/usr/bin/python3

'''
处理新概念语料（nce），这个文件直接处理1-4册全部的语料， 将语料写到4个csv文件中

'''

from textblob import TextBlob

#通过访问nce[2]就可以得到第二册有多少课文
nce_len = [0,0,96,60,60]

#生成01开始到99(end)结束的字符数组,包含end
def strlist(end):
    result = []
    for i in range(end+1):
        if i == 0:
            continue

        istr = str(i)
        if i <=9:
            istr = '0'+istr

        result.append(istr)

    return result
        
#处理第一册，因为第一册就一个文件
def nce1():
    print("处理第一册")
    f = open("../../nce/nce1all.txt")
    lines = f.readlines()

    nosplit = [i.strip() for i in lines if len(i.strip())>2]

    return nosplit

    

    
#处理第二-四册
def nce2(num):
    #找到有多少课文
    nl = nce_len[num]

    #生成序列
    text_list = strlist(nl)

    #结果文件
    texts = []

    #
    suffix = ".txt" if num!=4 else ".TXT"
    for t in text_list:
        #整个文件名
        text_name = "../../nce/nce%s/%s%s"%(num,t,suffix)
        print("文件名",text_name)
        f = open(text_name)
        
        lines = f.readlines()

        lines = [i.strip() for i in lines if len(i.strip())>2]

        new_lines = ""
        
        #去掉结尾的-，这玩意是连字符
        for (indx,line) in enumerate(lines):
            line = line.strip()
            if line[-1] == '-':
                new_lines += line[:-1]
            else:
                new_lines += line
                new_lines += " "
            
        #建立
        blob = TextBlob(new_lines)

        #得到句子
        sentences = blob.sentences

        for sent in sentences:
            tw = str(sent)
            texts.append(tw)

    return texts

if __name__ == '__main__':
    texts = [nce1(),nce2(2),nce2(3),nce2(4)]

    for indx,text in enumerate(texts):
        target = open("../../data/nce/nce%s.txt"%(indx+1),"w")
        for t in text:
            target.write("%s\n"%(t))

    

    
