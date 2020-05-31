#!/usr/bin/env python3

import pandas as pd
import random
import numpy as np
import time
import sys
import os
import networkx as nx
import pickle as pkl

dir_path = sys.argv[1].rstrip('/')
output_dir = dir_path + "_csr"

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

graphs = [
        # ('ENZYMES'                   , 18       , 6) ,
        # ('PROTEINS_full'             , 29       , 2) ,   
        # ('YeastH'                    , 75       , 2) ,   
        # ('OVCAR-8H'                  , 66       , 2) ,   
        # ('SW-620H'                   , 66       , 2) ,
        # ('Yeast'                     , 74       , 2) ,
        # ('DD'                        , 89       , 2) ,
        # ('COLLAB'                    , 100      , 3) ,
        # ('TWITTER-Real-Graph-Partial', 1323     , 2) ,   

        ( 'Reddit'                   , 602    , 41),
        ( 'amazon0505'               , 96	  , 22),
        ( 'artist_edges'             , 100	  , 12),
        ( 'com-amazon'               , 96	  , 22),
        ( 'web-BerkStan'             , 100	  , 12),
        ( 'wiki-topcats'             , 300	  , 12),
        ( 'soc-BlogCatalog'	         , 128	  , 39  ),      
        ( 'NELL'	                 , 5414	  , 210 ),      

        # ('enwiki-2013'	           , 100	, 12),
        # ( 'amazon_also_bought'       , 96     , 22),
        # ( 'amazon_also_viewed'       , 96     , 22),      
        # ('citeseer'	        , 3703	    , 6   ),  
        # ('cora' 	        , 1433	    , 7   ),  
        # ('pubmed'	        , 500	    , 3   ),      
        # ('ppi'	            , 50	    , 121 ),      
        # ('ms_academic'	    , 500	    , 25  ),      
        # ('amazon0601'  	    , 96	    , 22  ), 
] 

for idx in range(len(graphs)):
    print(graphs[idx])
    fname, _, _ = graphs[idx]
    if 'orig' in dir_path:
        os.system("cp {} {}".format(dir_path + "/" + fname + ".el" , output_dir + "/" + fname))
        os.system("tools/text_to_bin.bin {} 0 0 16".format(output_dir+"/"+fname))
    else:
        os.system("cp {} {}".format(dir_path + "/" + fname, output_dir + "/" + fname))
        os.system("tools/text_to_bin.bin {} 0 0 16".format(output_dir+"/"+fname))