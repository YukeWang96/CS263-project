#!/usr/bin/env python3
import time
import os
import sys
import threading 

import scipy
from scipy import io
from scipy.sparse import coo_matrix

src_dir = "orig/"
trg_dir = "orig-mtx/"

def read_COO(graph_path):
    fp = open(graph_path)
    row = []
    col = []
    point_set = set()

    for line in fp:
        tmp = line.rstrip("\n").split()
        src, trg = int(tmp[0]), int(tmp[1])
        row.append(src)
        col.append(trg)
        point_set.add(src)
        point_set.add(trg)

    data = [1] * len(row)
    n_points = max(point_set) + 1
    return coo_matrix((data, (row, col)), shape=(n_points, n_points))

def method_func(gr):
    graph_path, output_path = src_dir + gr + ".el", trg_dir + gr + ".mtx"
    graph_COO = read_COO(graph_path)
    io.mmwrite(output_path, graph_COO, symmetry='general')


if __name__ == "__main__":

    graphs = [
        # 'ENZYMES'                   ,
        # 'PROTEINS_full'             ,

        # 'YeastH'                    ,
        # 'OVCAR-8H'                  ,
        # 'SW-620H'                   ,
        # 'Yeast'                     ,
        # 'DD'                        ,
        # 'COLLAB'                    ,
        # 'TWITTER-Real-Graph-Partial',
        # 'Reddit'                    ,

        # 'amazon0505'                ,
        # 'artist_edges'              ,
        # 'com-amazon'                ,
        # 'web-BerkStan'              ,
        # 'wiki-topcats'              ,

        # 'amazon_also_bought'        ,
        # 'amazon_also_viewed'        ,
        # 'enwiki-2013'               ,

        'REDDIT-BINARY'             ,         
		'REDDIT-MULTI-12K'          ,         
		'REDDIT-MULTI-5K'           ,
    ]
    
    for idx in range(0, len(graphs), 4):
        print("=> " + graphs[idx])
        t1 = threading.Thread(target=method_func, args=(graphs[idx],))
        t1.start() 

        if idx + 1 < len(graphs):
            print("=> "+ graphs[idx + 1]) 
            t2 = threading.Thread(target=method_func, args=(graphs[idx + 1],)) 
            t2.start()
        
        if idx + 2 < len(graphs):
            print("=> "+ graphs[idx + 2]) 
            t3 = threading.Thread(target=method_func, args=(graphs[idx + 2],)) 
            t3.start()

        if idx + 3 < len(graphs):
            print("=> "+ graphs[idx + 3]) 
            t4 = threading.Thread(target=method_func, args=(graphs[idx + 3],)) 
            t4.start()
        
        if idx + 4 < len(graphs):
            print("=> "+ graphs[idx + 4]) 
            t5 = threading.Thread(target=method_func, args=(graphs[idx + 4],)) 
            t5.start()    
    
        t1.join()
        if idx + 1 < len(graphs):
            t2.join()
        
        if idx + 2 < len(graphs):
            t3.join()

        if idx + 3 < len(graphs):
            t4.join()
        
        if idx + 4 < len(graphs):
            t5.join()
            
        print("-----------------------------") 
  
    print("Done!!!") 