#!/usr/bin/env python3
import subprocess
import os
import sys

# graph_dir = "../datasets/pyG/trans-prep/"
# graph_dir = "../datasets/pyG/orig-prep/"
# graph_dir = "../datasets/large/orig/"
graph_dir = "../datasets/large/trans/"

subprocess.run(["rm", "-rf", "{}*.bin".format(graph_dir)])

files = os.listdir(graph_dir)
for fname in files:
    print(fname)
    subprocess.run(["./text_to_bin.bin", graph_dir+"{}".format(fname), "0", "0", "16"])

print("=> Completed !!!")