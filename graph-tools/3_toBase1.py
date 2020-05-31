#!/usr/bin/env python3
import os
import sys

graphs = [
        ('COLLAB'                    , 372474  ),
        ('DD'                        , 334925  ),
        ('ENZYMES'                   , 19327   ),
        ('OVCAR-8H'                  , 1890931 ),   
        ('PROTEINS_full'             , 43471   ),   
        ('SW-620H'                   , 1889971 ),
        ('TWITTER-Real-Graph-Partial', 580768  ),   
        ('Yeast'                     , 1714644 ),
        ('YeastH'                    , 3139988 ),   

        ( 'Reddit'                   , 232965  ),
        ( 'amazon0505'               , 410236  ),
        ( 'artist_edges'             , 50515   ),
        ( 'com-amazon'               , 334863  ),
        ( 'web-BerkStan'             , 685230  ),
        ( 'wiki-topcats'             , 1791489 ),
        
        ('citeseer'	                 , 3327    ),  
        ('cora' 	                 , 2708    ),  
        ('pubmed'	                 , 19717   ),      
        ('NELL'	                     , 75492   ),      
        ('ppi'	                     , 56944   ),      
        ('ms_academic'	             , 18333   ),      
        ('soc-BlogCatalog'	         , 88784   ),      
        ('amazon0601'  	             , 403394  ), 
]

src_dir = sys.argv[1]
trg_dir = src_dir.strip("/") + "-base1"

if not os.path.exists(trg_dir):
    os.mkdir(trg_dir)

for gr, _ in graphs:
    print(gr)
    fin = open("{}/{}.el".format(src_dir, gr))
    fout = open("{}/{}".format(trg_dir, gr), "w")
    for line in fin:
        tmp = line.rstrip("\n").split()
        src, trg = int(tmp[0]) + 1, int(tmp[1]) + 1
        fout.write("{} {}\n".format(src, trg))
    fin.close()
    fout.close()