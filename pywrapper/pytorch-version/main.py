import torch
import argparse
import numpy as np
from graph import graph
import torch.nn.functional as F
from graph import graph
from virtual_graph import vgraph



parser = argparse.ArgumentParser(description='GNN Pytorch')
parser.add_argument('--graph_path', type=str,
                    help='path of GNN graph file in coo')
parser.add_argument('--feature', type=int, defualt=100,
                    help='size of feature embedding')
parser.add_argument('--hidden', type=int, defualt=16,
                    help='size of hidden dimension of GNN network')
parser.add_argument('--classes', type=int, defualt=10,
                    help='size of the output classes')
args = parser.parse_args()


if __name__ == "__main__":
    print(args)