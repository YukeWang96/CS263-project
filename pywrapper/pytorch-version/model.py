# import SAG_kernel
import torch.nn.functional as F
import torch

class GCN(object):
    def __init__(self, n_feature, n_hidden, n_class, n_hidden_layers=1):
        self.n_feature = n_feature
        self.n_hidden = n_hidden
        self.n_class = n_class
        self.n_hidden_layers = n_hidden_layers
        # self.aggre = SAG_kernel()
        self.head_update = torch.nn.Linear(n_feature, n_hidden, bias=True)
        self.hidden_update = torch.nn.Linear(n_hidden, n_hidden, bias=True)
        self.tail_update = torch.nn.Linear(n_hidden, n_class, bias=True)
        

    def forward(self, graph_obj):

        numGroups, nodePointer, n_hidden, \
            numNodes, groupNodePointer, edgeList, embed = graph_obj

        # out = self.head_update(feature_embedding)
        # x = torch.zeros((numNodes, n_hidden))
        # self.aggre(numGroups, nodePointer, n_hidden,
        #            numNodes, groupNodePointer, edgeList,
        #             x, out)

        print(embed.size())
        # print(self.head_update)        
        x = self.head_update(embed)

        x = F.relu(x)
        print(x.size())

        for hid in range(self.n_hidden_layers - 1):
            # out = self.hidden_update(x)
            # x = torch.zeros((numNodes, n_hidden))
            # self.aggre(numGroups, nodePointer, n_hidden,
            #           numNodes, groupNodePointer, edgeList,
            #            x, out)
            x = self.hidden_update(x)
            x = F.relu(x)
        
        x = self.tail_update(x)
        x = F.relu(x)
        
        print(x.size())

        return F.log_softmax(x, dim=-1)