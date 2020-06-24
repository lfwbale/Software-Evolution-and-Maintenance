import pickle
import time
import requests
from bs4 import BeautifulSoup
import random

def read_file(path):
    with open(path, 'r') as f:
        for line in f:
            yield line

def gen_dic(begin, end, path):
    cnt = 0
    dic = {}
    for line in read_file('../baike_triples.txt'):
        cnt += 1
        if cnt > begin:
            node_1, relationship, node_2 = line.strip().split('\t')
            dic.setdefault(node_1, {}).setdefault(relationship, []).append(node_2)
            if cnt%5000000 == 0:
                print(cnt)
        if cnt == end or line == '':
            break
    
    print("dumping...")
    with open(path, 'wb') as f:
        pickle.dump(dic, f)
    #print(dic)
    print("done")
    


if __name__ == "__main__":
    for i in range(15):
        begin = 5000000*i
        end = begin+5000000
        path = '../dic/dic_test'+str(i+1)
        gen_dic(begin, end, path)
