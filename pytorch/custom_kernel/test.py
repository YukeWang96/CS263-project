import torch
import numpy as numpy

import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from gcn import GCN_SAG

def test_gcn_forward():
    numNodes = 3
    ebd_dim = 3
    numParts = 6
    embed_input = torch.ones(numNodes,ebd_dim) # number of nodes by edb_dim
    edgeList = torch.ones(1, 9).int() # number of nodes + number of edge
    nodePointer = torch.ones(1,numNodes).int()
    partNodePointer = torch.ones(6,2).int() # number of edges by 2
    gcn_f = GCN_SAG.apply
    output = gcn_f(nodePointer, edgeList, partNodePointer, embed_input, numParts, ebd_dim, numNodes)

    print(output)

if __name__ == '__main__':
    test_gcn_forward()

