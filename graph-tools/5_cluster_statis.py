#!/usr/bin/env python3
import os
import sys
import collections
import math
import numpy

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# files = os.listdir(sys.argv[1])
graphs = [
        ('Reddit'           ),
        ('amazon0505'       ),
        ('artist_edges'     ),
        ('com-amazon'       ),
        ('wiki-topcats'     ),
        ('soc-BlogCatalog'	),   
        ('amazon0601'  	    ),
]

print("graph, min, max, std, mean, median")
for fname in graphs:
    fp = open(os.path.join(sys.argv[1], fname), "r")
    node2clusters = collections.defaultdict(list)
    nid = 0
    for line in fp:
        cid = int(line.strip("\n"))
        nid += 1
        node2clusters[cid].append(nid)
    
    x = []
    for nid in node2clusters.keys():
        x.append(len(node2clusters[nid]))
    
    print(fname, end=",")
    print("{:.0f}".format(numpy.min(x)), end=",")
    print("{:.0f}".format(numpy.max(x)), end=",")
    print("{:.3f}".format(numpy.std(x)), end=",")
    print("{:.3f}".format(numpy.mean(x)), end=",")
    print("{:.0f}".format(numpy.median(x)))

    # sns.set(color_codes=True)
    # sns.distplot(x, kde=False)
    plt.title('{}'.format(fname))
    plt.xlabel('cluster size')
    plt.ylabel('#clusters')
    plt.hist(x, bins=30)
    # plt.show()
    plt.savefig('{}.png'.format(fname))
    # plt.clear()
    plt.close()