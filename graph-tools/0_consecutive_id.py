#!/usr/bin/env python3

"""@encode_consecutive_id
convert graph with discountine node ids to continuous id start from 0
"""
import pandas as pd
import random
import numpy as np
import time
import sys
import os

def encode_consecutive_id(dir_path):
    '''convert graph with discountine node ids to continuous id start from 0
    Args:
        dir_path: the path to the directory of graph files (COO format).
    
    Returns:
        None.

    Note: 
        After the function return, the priginal graph files are renamed 
        to '*.old' under the same directory along with the new graphs. 
    '''
    dir_path = 
    files = os.listdir(dir_path)

    for fname in files:
        
        print(fname)
        os.system("mv {} {}".format(os.path.join(dir_path, fname), os.path.join(dir_path, fname + ".old")))
        fin = open(os.path.join(dir_path, fname + ".old"), "r")
        fout = open(os.path.join(dir_path, fname), "w")

        edges = []
        for line in fin:
            tmp = line.rstrip("\n").split()
            src, trg = int(tmp[0]), int(tmp[1])
            edges.append((src, trg))
        
        fin.close()
        edges.sort(key=lambda x: x[0])

        edges_src = []
        tmp_trg = []
        node_dict = {}
        cnt = 0
        
        for e in edges:
            src, trg = e[0], e[1]
            if src not in node_dict:
                node_dict[src] = cnt
                src = cnt
                cnt += 1
            else:
                src = node_dict[src]
            edges_src.append(src)
            tmp_trg.append(trg)
        
        for src, trg in zip(edges_src, tmp_trg):
            if trg not in node_dict:
                node_dict[trg] = cnt
                trg = cnt
                cnt += 1
            else:
                trg = node_dict[trg]
            fout.write("{} {}\n".format(src, trg))
        fout.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError('Usage: ./exe dir_with_graphs.txt')
    dir_pth = sys.argv[1].rstrip('/')
    encode_consecutive_id(dir_pth)