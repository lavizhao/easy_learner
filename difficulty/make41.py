#!/usr/bin/python3

import csv
from random import random

data_dir = "../../data/nce/nce"
suffix = ".txt"
target = "../../data/nce/nce.csv"

cs = ["1","2","3","4"]

t = open(target,"w")
writer = csv.writer(t)

if __name__ == '__main__':
    fi = [open(data_dir+i+suffix) for i in cs]

    end = [0,0,0,0]
    count = 0
    while True:
        if sum(end) == 4:
            break;
            
        line = fi[count].readline()
        if line :
            writer.writerow([line.strip(),count+1])
        else:
            end[count] = 1

        count += 1
        count = count % 4
        
