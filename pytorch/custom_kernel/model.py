import torch
import torch.nn as nn
import torch.nn.functional as F
import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from gcn import GCN_SAG

class GCN(nn.Module):
    def __init__(self, n_feature, n_hidden, n_class, n_hidden_layers=1):
        super(GCN, self).__init__()
        self.n_feature = n_feature
        self.n_hidden = n_hidden
        self.n_class = n_class
        self.n_hidden_layers = n_hidden_layers
        self.head_update = torch.nn.Linear(n_feature, n_hidden, bias=True)
        self.hidden_update = torch.nn.Linear(n_hidden, n_hidden, bias=True)
        self.tail_update = torch.nn.Linear(n_hidden, n_class, bias=True)
        self.aggre = GCN_SAG.apply

    def forward(self, numGroups, nodePointer, ebd_dim, numNodes, groupNodePointer, edgeList, embed):

        # numGroups, nodePointer, n_hidden, \
        #     numNodes, groupNodePointer, edgeList, embed = graph_obj

        x = self.head_update(embed)
        x = self.aggre(nodePointer, edgeList, groupNodePointer, x,
                     numGroups, self.n_hidden, numNodes)

        # print(x.size())
        # print(self.head_update)        
        # x = self.head_update(embed)
        x = F.relu(x)
        # print(x.size())

        for hid in range(self.n_hidden_layers - 1):
            x = self.hidden_update(x)
            x = self.aggre(nodePointer, edgeList, groupNodePointer, 
                        x, numGroups, n_hidden, numNodes)
            x = F.relu(x)
        
        x = self.tail_update(x)
        x = F.relu(x)
        # print(x.size())

        return F.log_softmax(x, dim=-1)

class GCN_spMM(nn.Module):
    def __init__(self, n_feature, n_hidden, n_class,            n_hidden_layers=1):
        super(GCN_spMM, self).__init__()
        self.n_feature = n_feature
        self.n_hidden = n_hidden
        self.n_class = n_class
        self.n_hidden_layers = n_hidden_layers
        self.head_update = torch.nn.Linear(n_feature, n_hidden, bias=True)
        self.hidden_update = torch.nn.Linear(n_hidden, n_hidden, bias=True)
        self.tail_update = torch.nn.Linear(n_hidden, n_class, bias=True)

    def forward(self, graph_sparse_coo, embed):

        x = self.head_update(embed)
        x = torch.sparse.mm(graph_sparse_coo, x)
        x = F.relu(x)

        for hid in range(self.n_hidden_layers - 1):
            x = self.hidden_update(x)
            x = torch.sparse.mm(graph_sparse_coo, x)
            x = F.relu(x)
        
        x = self.tail_update(x)
        x = F.relu(x)

        return F.log_softmax(x, dim=-1)