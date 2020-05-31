#!/usr/bin/env python3
import os
import sys

graph = [
    'amazon0601',
    'soc-BlogCatalog',
]

for gr in graph:
    os.system("mv {} {}".format("{}/{}.el".format(sys.argv[1], gr), "{}/{}_base1.el".format(sys.argv[1], gr)))
    fp = open("{}/{}_base1.el".format(sys.argv[1], gr))
    fout = open("{}/{}.el".format(sys.argv[1], gr), "w")
    print(gr)
    for line in fp:
        tmp = line.rstrip("\n").split()
        src, trg = int(tmp[0]) - 1, int(tmp[1]) - 1
        fout.write("{} {}\n".format(src, trg))
    fp.close()
    fout.close()