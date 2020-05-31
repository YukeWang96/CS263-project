#!/usr/bin/env python
import os
import sys
import statistics as st
import collections

files = os.listdir(sys.argv[1])
fs = [fname for fname in files if fname.endswith(".txt")]

for fname in sorted(fs):
    fp = open(os.path.join(sys.argv[1], fname))
    graph = collections.defaultdict(list)
    for line in fp:
        li = line.rstrip('\n').split()
        src, trg = li[0], li[1]
        graph[src].append(trg)
        graph[trg].append(src)
    
    box = []
    for nid in graph.keys():
        box.append(len(graph[nid]))

    print("{}, {}".format(fname, st.pstdev(box)))