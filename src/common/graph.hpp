#ifndef GRAPH_HPP
#define GRAPH_HPP

#include <iostream>
#include <stdlib.h>
#include <ctime>
#include <fstream>
#include <string>
#include <ctime>
#include <random>
#include <stdio.h>
#include <iomanip>
#include <locale>
#include <sstream>
#include <string>
#include <cstring>
#include <vector>
#include <cstdlib>
#include <math.h>
#include <chrono>
#include <iterator>

// #include "globals.hpp"

typedef unsigned int uint;
using namespace std;

class Graph
{
private:

public:
	string graphFilePath;
    string graphEmbdPath;
	bool isWeighted;
	bool hasZeroID;
	uint num_nodes;
	uint num_edges;
    vector<Edge> edges;
    vector<Embedding> pt_embeds;
    vector<uint> weights;
    bool graphLoaded;
    Graph(string graphFilePath, string graphEmbdPath, bool isWeighted);
    void ReadGraph();
    void ReadEmbedding();
};

#endif	//	GRAPH_HPP



