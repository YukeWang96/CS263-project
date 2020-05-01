#!/usr/bin/env python3
import networkx as nx
import metis
import pickle
import os, sys
# import pydot
# from networkx.drawing.nx_pydot import write_dot

times = 1
graphs = [
        # ('COLLAB'                    ,  5000   ),
        # ('DD'                        ,  1209   ),
        # ('ENZYMES'                   ,  640    ),
        # ('OVCAR-8H'                  ,  44447  ),
        # ('PROTEINS_full'             ,  1195   ),
        # ('SW-620H'                   ,  44470  ),
        # ('TWITTER-Real-Graph-Partial',  147179 ),
        # ('Yeast'                     ,  84310  ),
        # ('YeastH'                    ,  86180  ),

        ('Reddit'                   , 187 * times),
        ('amazon0505'               , 53  * times),
        ('artist_edges'             , 7   * times),
        ('com-amazon'               , 43  * times),
        ('wiki-topcats'             , 707  * times),
        ('soc-BlogCatalog'	        , 15  * times),
        ('amazon0601'  	            , 52  * times),

        # ('citeseer'	                 ,  456    ),  
        # ('cora' 	                 ,  96     ),  
        # ('pubmed'	                 ,  18     ),      
        # ('NELL'	                     ,  8605   ),      
        # ('ppi'	                     ,  295    ),      
        # ('ms_academic'	             ,  12     ),      
        # ('soc-BlogCatalog'	         ,  5      ),      
        # ('amazon0601'  	             ,  63     ), 
]

indir = sys.argv[1]
outdir = indir.rstrip("/").rstrip("_pkl") + "_metis_part"
if not os.path.exists(outdir):
    os.mkdir(outdir)

for gr, npart in graphs:
    print(gr)
    fp = open(os.path.join(indir, gr+".pkl"), "rb")
    fout = open(os.path.join(outdir, gr+".part"), "w")
    G = pickle.load(fp)
    (edgecuts, parts) = metis.part_graph(G, npart)

    for nid, partid in enumerate(parts):
        fout.write("{}\n".format(partid))