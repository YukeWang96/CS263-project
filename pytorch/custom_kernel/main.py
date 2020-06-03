import torch
import torch.nn as nn
import argparse
import numpy as np
import torch.nn.functional as F
import time

from graph import graph
from virtual_graph import vgraph
from model import GCN, GCN_spMM

parser = argparse.ArgumentParser(description='GNN Pytorch')
parser.add_argument('--graph_path', type=str,
                    help='path of GNN graph file in coo')
parser.add_argument('--feature', type=int, default=100,
                    help='size of feature embedding')
parser.add_argument('--hidden', type=int, default=16,
                    help='size of hidden dimension of GNN network')
parser.add_argument('--classes', type=int, default=10,
                    help='size of the output classes')
parser.add_argument('--kernel', type=str, default="SAG",
                    help='GNN kernel options: auto (default), SAG, SpMM')
parser.add_argument('--gpu', action='store_true',
                    help='set if use GPU, otherwise CPU')
args = parser.parse_args()


def toTorchTensor(virtual_graph, gpu=False):
    numGroups = int(virtual_graph.numGroups)
    nodePointer = torch.from_numpy(virtual_graph.nodePointer).unsqueeze(0).int()
    ebd_dim = int(args.feature)
    numNodes = int(virtual_graph.n_nodes)
    groupNodePointer = torch.from_numpy(virtual_graph.groupNodePointer).int()
    edgeList = torch.from_numpy(virtual_graph.edgeList).unsqueeze(0).int()
    embed = torch.rand(virtual_graph.n_nodes, args.feature)

    return numGroups, nodePointer, ebd_dim, numNodes, groupNodePointer, edgeList, embed


def toTorchTensor_spMM(graph, gpu=False):
    # fp = open(graph_path)
    # for line in fp:
    #     tmp = line.strip('\n').split(" ")
    #     a, b = int(tmp[0]), int(tmp[1])
    #     src.append(a)
    #     trg.append(b)

    src = graph.src_li
    trg = graph.trg_li
    val = torch.ones(len(src))
    n_nodes = len(set(src + trg))
    idx = torch.LongTensor([src, trg])

    graph_coo = torch.sparse.FloatTensor(idx, val, torch.Size([n_nodes, n_nodes]))
    embed = torch.rand((n_nodes, args.feature))

    print("#V:{}\t#E:{}".format(n_nodes, len(src)))
    return graph_coo, embed 

def SAG_routine(G):
    start = time.perf_counter()
    vG = vgraph(G)
    vG.make_vgraph()
    vG.print_vgraph()
    numGroups, nodePointer, ebd_dim, numNodes, groupNodePointer, edgeList, embed = toTorchTensor(vG, args.gpu)
    gcn = GCN(args.feature, args.hidden, args.classes)

    if args.gpu:
        gcn = gcn.cuda()
        nodePointer = nodePointer.cuda()
        groupNodePointer = groupNodePointer.cuda()
        edgeList = edgeList.cuda()
        embed = embed.cuda()

    end1 = time.perf_counter()
    gcn(numGroups, nodePointer, ebd_dim, numNodes, groupNodePointer, edgeList, embed)
    end2 = time.perf_counter()
    overall = end2 - start
    cpu_side = (end1 - start)/overall * 100
    mode_side = (end2 - end1)/overall * 100
    print("--Host, {:.2f}%, Model, {:.2}%".format(cpu_side, mode_side))

def SpMM_routine(G):
    graph_coo, embed = toTorchTensor_spMM(G, args.gpu)
    start = time.perf_counter()
    gcn_spmm = GCN_spMM(args.feature, args.hidden, args.classes)
    if args.gpu:
        gcn_spmm = gcn_spmm.cuda()
        graph_coo = graph_coo.cuda()
        embed = embed.cuda()

    end1 = time.perf_counter()
    gcn_spmm(graph_coo, embed)

    end2 = time.perf_counter()
    overall = end2 - start
    cpu_side = (end1 - start)/overall * 100
    mode_side = (end2 - end1)/overall * 100
    print("--Host, {:.2f}%, Model, {:.2}%".format(cpu_side, mode_side))

if __name__ == "__main__":

    G = graph()
    G.read_graph_files(args.graph_path)
    G.kernel_choice()

    if args.kernel == 'auto':
        print("--AUTO Select [ {} ] Kernel".format(G.kernel))
    else:
        print("--MANUAL Select [ {} ] Kernel".format(args.kernel))

    if args.kernel == 'auto':
        if G.kernel == "SAG":
            SAG_routine(G)
        else:
            SpMM_routine(G)
    else:
        if args.kernel == 'SAG':
            SAG_routine(G)
        else:
            SpMM_routine(G)
    print()