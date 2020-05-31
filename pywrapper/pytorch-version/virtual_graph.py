from graph import graph

class vgraph(object):
    def __init__(self, graph):
        self.orig_graph = graph

        self.n_nodes = self.orig_graph.n_nodes
        self.n_edges = self.orig_graph.n_edges
        
        self.edgeList = np.zeros(self.n_nodes + self.n_edges)
        self.nodePointer = np.zeros(self.n_nodes)
        self.inDegree = np.zeros(self.n_nodes)
        self.numGroups = 0
        self.groupNodePointer = None

        self.Partsize = 1
        self.numGroups = 0

    def make_vgraph(self):

        # node pointer counter
        counter = 0
        for i in range(self.n_nodes):
            self.nodePointer[i] = counter
            edgeList[counter] = self.inDegree[i]

            if self.inDegree[i] % self.Partsize == 0:
                self.numGroups += self.inDegree[i]/self.Partsize 
            else:
                self.numGroups += self.inDegree[i]/self.Partsize + 1

            counter = coutner + self.inDegree[i] + 1

        self.groupNodePointer = np.zeros((self.numGroups, 2))
        inDegreeCounter = np.zeros(self.n_nodes)

        for i in range(self.n_nodes):
            for nid in self.orig_graph.graph_dict[i]:
                loc = self.nodePointer[i] + 1 + inDegreeCounter[i]
                self.edgeList[loc] = nid
                inDegreeCounter[i] += 1

        counterParts = 0
        for i in range(self.n_nodes):
            if self.inDegree[i] % self.Partsize == 0:
                currGroups = self.inDegree[i]/self.Partsize
            else:
                currGroups = self.inDegree[i]/self.Partsize + 1

            for j in range(currGroups):
                self.groupNodePointer[counterParts][0] = i
                self.groupNodePointer[counterParts][1] = j
                counterParts += 1