# import SAG_kernel
import torch.nn.functional as F

class GCN(object):
    def __init__(self, n_feature, n_hidden, n_class, n_hidden_layers):
        self.n_feature = n_feature
        self.n_hidden = n_hidden
        self.n_class = n_class
        self.n_hidden_layers = n_hidden_layers
        # self.aggre = SAG_kernel()
        self.head_update = torch.nn.Linear(in_features, n_hidden, bias=True)
        self.hidden_update = torch.nn.Linear(n_hidden, n_hidden, bias=True)
        self.tail_update = torch.nn.Linear(n_hidden, out_features, bias=True)
        

    def forward(self, graph, feature_embedding):

        x = self.head_update(feature_embedding)
        # x = self.aggre(graph, x)
        x = F.relu(x)

        for hid in range(self.n_hidden_layers - 1):
            x = self.hidden_update(x)
            # x = self.aggre(graph, x)
            x = F.relu(x)
        
        x = self.tail_update(x)
        x = F.relu(x)

        return F.log_softmax(x, dim=-1)


        