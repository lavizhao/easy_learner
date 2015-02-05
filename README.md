# easy_learner
英语例句检索系统

#文件层级
1. `extractor` 为抽取文件, 抽取不同的语料, 现在暂定的是抽取multi-un的语料
2. `indexer`   为建索引的文件夹, 主要负责建立索引
3. `server`    为django的目录, 主要包含有django文件(这东西我没用过, 不知道怎么用),和lucene的检索函数
4. `util`      为常用函数放置, 比如一些NLP函数
