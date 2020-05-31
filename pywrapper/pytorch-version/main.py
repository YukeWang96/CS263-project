import torch
import argparse
import numpy as np
from graph import graph
import torch.nn.functional as F
from graph import graph
from virtual_graph import vgraph
from model import *

parser = argparse.ArgumentParser(description='GNN Pytorch')
parser.add_argument('--graph_path', type=str,
                    help='path of GNN graph file in coo')
parser.add_argument('--feature', type=int, default=100,
                    help='size of feature embedding')
parser.add_argument('--hidden', type=int, default=16,
                    help='size of hidden dimension of GNN network')
parser.add_argument('--classes', type=int, default=10,
                    help='size of the output classes')
# parser.add_argument('--device', type=int, default=0,
#                     help='gpu deivce id')
args = parser.parse_args()


def toTorchTensor(virtual_graph, gpu=False):
    numGroups = torch.IntTensor(virtual_graph.numGroups)
    nodePointer = torch.from_numpy(virtual_graph.nodePointer)
    ebd_dim = torch.IntTensor(args.feature)
    numNodes = torch.IntTensor(virtual_graph.n_nodes)
    groupNodePointer = torch.from_numpy(virtual_graph.groupNodePointer)
    edgeList = torch.from_numpy(virtual_graph.edgeList)
    embed1 = torch.zeros((virtual_graph.n_nodes, args.feature))
    embed2 = torch.rand(virtual_graph.n_nodes, args.feature)

    if gpu:
        numGroups.cuda()
        nodePointer.cuda()
        ebd_dim.cuda()
        numNodes.cuda()
        groupNodePointer.cuda()
        edgeList.cuda()
        embed1.cuda()
        embed2.cuda()


if __name__ == "__main__":
    # print(args.graph_path)
    G = graph()
    G.read_graph_files(args.graph_path)
    # G.gen_graph_embedding(args.feature)
    vG = vgraph(G)
    vG.make_vgraph()
    vG.print_vgraph()

    toTorchTensor(vG)
    print("Finished!")
    