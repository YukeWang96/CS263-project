from gcn import GCN_SAG
import torch.nn.functional as F
import torch

class GCN(object):
    def __init__(self, n_feature, n_hidden, n_class, n_hidden_layers=1):
        self.n_feature = n_feature
        self.n_hidden = n_hidden
        self.n_class = n_class
        self.n_hidden_layers = n_hidden_layers
        self.head_update = torch.nn.Linear(n_feature, n_hidden, bias=True)
        self.hidden_update = torch.nn.Linear(n_hidden, n_hidden, bias=True)
        self.tail_update = torch.nn.Linear(n_hidden, n_class, bias=True)
        self.gcn_aggre = GCN_SAG.apply

    def forward(self, graph_obj):

        numGroups, nodePointer, n_hidden, \
            numNodes, groupNodePointer, edgeList, embed = graph_obj

        x = self.head_update(embed)
        self.aggre(nodePointer, edgeList, groupNodePointer, x,
                     numGroups, n_hidden, numNodes)

        print(x.size())
        # print(self.head_update)        
        # x = self.head_update(embed)
        x = F.relu(x)
        # print(x.size())

        for hid in range(self.n_hidden_layers - 1):
            x = self.hidden_update(x)
            self.aggre(nodePointer, edgeList, groupNodePointer, 
                        x, numGroups, n_hidden, numNodes)
            x = F.relu(x)
        
        x = self.tail_update(x)
        x = F.relu(x)
        
        print(x.size())

        return F.log_softmax(x, dim=-1)