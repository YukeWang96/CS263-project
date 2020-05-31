from graph import graph
import numpy as np

class vgraph(object):
    def __init__(self, graph):
        self.orig_graph = graph

        self.n_nodes = self.orig_graph.n_nodes
        self.n_edges = self.orig_graph.n_edges
        self.graph_dict = self.orig_graph.graph_dict
        
        self.edgeList = np.zeros(self.n_nodes + self.n_edges, dtype=int)
        self.nodePointer = np.zeros(self.n_nodes, dtype=int)
        self.inDegree = np.zeros(self.n_nodes, dtype=int)
        self.groupNodePointer = None

        self.groupSize = 1
        self.numGroups = 0

        self._get_inDegree()
    
    def _get_inDegree(self):
        for idx, nbs in self.graph_dict.items():
            self.inDegree[idx] = len(nbs)

    def make_vgraph(self):

        # node pointer counter
        counter = 0
        for i in range(self.n_nodes):
            self.nodePointer[i] = counter
            self.edgeList[counter] = self.inDegree[i]

            if self.inDegree[i] % self.groupSize == 0:
                self.numGroups += int(self.inDegree[i]/self.groupSize) 
            else:
                self.numGroups += int(self.inDegree[i]/self.groupSize) + 1

            counter = counter + self.inDegree[i] + 1

        self.groupNodePointer = np.zeros(shape=[self.numGroups, 2], dtype=int)
        inDegreeCounter = np.zeros(self.n_nodes, dtype=int)

        for i in range(self.n_nodes):
            for nid in self.orig_graph.graph_dict[i]:
                loc = self.nodePointer[i] + 1 + inDegreeCounter[i]
                self.edgeList[loc] = nid
                inDegreeCounter[i] += 1

        counterParts = 0
        for i in range(self.n_nodes):
            if self.inDegree[i] % self.groupSize == 0:
                currGroups = int(self.inDegree[i]/self.groupSize)
            else:
                currGroups = int(self.inDegree[i]/self.groupSize) + 1

            for j in range(currGroups):
                self.groupNodePointer[counterParts][0] = i
                self.groupNodePointer[counterParts][1] = j
                counterParts += 1

    def print_vgraph(self):
        print(self.groupNodePointer)
        for i in range(len(self.groupNodePointer)):
            nid, pid = self.groupNodePointer[i][0], self.groupNodePointer[i][1]
            print("global_partID: {}, nid: {}, local_partID: {}".format(i, nid, pid))