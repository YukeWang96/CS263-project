import os
import sys
import collections
import numpy as np

class graph(object):
    def __init__(self):
        self.n_nodes = 0
        self.n_edges = 0
        self.n_feature = 0
        self.graph_dict = collections.defaultdict(list)
        self.feature_embed = None

    def read_graph_files(self, graph_path):
        assert os.path.exists(graph_path)
        assert not os.path.isdir(graph_path)
            
        fp = open(graph_path, "r")        
        for line in fp:
            tmp = line.strip("\n").split(' ')
            src, trg = int(tmp[0]), int(tmp[1])
            self.graph_dict[trg].append(src)
            self.n_edges += 1
        self.n_nodes = len(self.graph_dict)
        print("#V:{}\t#E:{}".format(self.n_nodes, self.n_edges))

    def gen_graph_embedding(self, n_features):
        self.n_feature = n_features
        self.feature_embed = np.random.rand(self.nodes, self.n_feature)