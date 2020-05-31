#include "virtual_graph.hpp"

// #include <tuple>
// #include <queue> 
#include <cmath>

using namespace std;
// #define PART_OPT

VirtualGraph::VirtualGraph(Graph &graph)
{
	if(graph.hasZeroID == false)
	{
		#pragma omp parallel for
		for(int i=0; i<graph.num_edges; i++)
		{
			graph.edges[i].source = graph.edges[i].source - 1;
			graph.edges[i].end = graph.edges[i].end - 1;
		}
	}
	
	this->graph = &graph;
	
	inDegree  = new uint[graph.num_nodes];
	outDegree  = new uint[graph.num_nodes];
	
	#pragma omp parallel for
	for(int i=0; i<graph.num_nodes; i++)
	{
		outDegree[i] = 0;
		inDegree[i] = 0;
	}
	
	#pragma omp parallel for
	for(int i=0; i<graph.num_edges; i++)
	{
		unsigned int src = graph.edges[i].source;
		unsigned int end = graph.edges[i].end;
		
		#pragma omp atomic
		outDegree[src]++;
		#pragma omp atomic
		inDegree[end]++;
	}
	
}
	
void VirtualGraph::MakeGraph()
{ 
	nodePointer = new uint[graph->num_nodes];
	edgeList = new uint[2*graph->num_edges + graph->num_nodes];
	
	uint *outDegreeCounter;
	uint source;
	uint end;
	uint w8;		
	
	long long counter=0;
	numParts = 0;
	int numZero = 0;
	for(int i=0; i<graph->num_nodes; i++)
	{
		nodePointer[i] = counter;
		edgeList[counter] = outDegree[i];
		
		if(outDegree[i] == 0)
			numZero++;
		
		if(outDegree[i] % Part_Size == 0)
			numParts += outDegree[i] / Part_Size ;
		else
			numParts += outDegree[i] / Part_Size + 1;
		
		counter = counter + outDegree[i]*2 + 1;
	}

	outDegreeCounter  = new uint[graph->num_nodes];
	
	for(int i=0; i<graph->num_edges; i++)
	{

		source = graph->edges[i].source;
		end = graph->edges[i].end;
		w8 = graph->weights[i];
		
		uint location = nodePointer[source]+1+2*outDegreeCounter[source];

		edgeList[location] = end;
		edgeList[location+1] = w8;

		outDegreeCounter[source]++;  
	}
	

	partNodePointer = new PartPointer[numParts];
	int thisNumParts;
	long long countParts = 0;

	for(int i=0; i<graph->num_nodes; i++)
	{
		if(outDegree[i] % Part_Size == 0)
			thisNumParts = outDegree[i] / Part_Size ;
		else
			thisNumParts = outDegree[i] / Part_Size + 1;

		for(int j=0; j<thisNumParts; j++)
		{
			partNodePointer[countParts].node = i;
			partNodePointer[countParts++].part = j;
		}
	}
}

void VirtualGraph::MakeUGraph()
{ 
	nodePointer = new uint[graph->num_nodes];
	edgeList = new uint[graph->num_edges + graph->num_nodes];
	
	uint *outDegreeCounter;
	uint source;
	uint end;
	uint w8;		
	
	long long counter=0;
	numParts = 0;
	int numZero = 0;

	outDegreeCounter  = new uint[graph->num_nodes];
	for(int i = 0; i < graph->num_nodes; i++)
	{
		outDegreeCounter[i] = 0;
		nodePointer[i] = counter;
		edgeList[counter] = outDegree[i];
		
		if(outDegree[i] == 0)
			numZero++;
		
		if(outDegree[i] % Part_Size == 0)
			numParts += outDegree[i] / Part_Size ;
		else
			numParts += outDegree[i] / Part_Size + 1;
		// printf("nid: %d, nparts: %d\n", i, outDegree[i] / Part_Size + 1);
		counter = counter + outDegree[i] + 1;
	}

	// std::cout << "numParts: " << numParts << std::endl;
	// outDegreeCounter  = new uint[graph->num_nodes];
	
	for(int i=0; i < graph->num_edges; i++)
	{
		source = graph->edges[i].source;
		end = graph->edges[i].end;
		
		// std::cout << source << " " << end << std::endl;
		uint location = nodePointer[source] + 1 + outDegreeCounter[source];
		// std::cout << outDegreeCounter[source] << std::endl;
		// std::cout << location << std::endl;
		edgeList[location] = end;
		outDegreeCounter[source]++;  
	}
	
	partNodePointer = new PartPointer[numParts];
	int thisNumParts;
	long long countParts = 0;

#ifndef PART_OPT
	for(int i=0; i<graph->num_nodes; i++)
	{
		if(outDegree[i] % Part_Size == 0)
			thisNumParts = outDegree[i] / Part_Size ;
		else
			thisNumParts = outDegree[i] / Part_Size + 1;

		for(int j=0; j<thisNumParts; j++)
		{
			partNodePointer[countParts].node = i;
			partNodePointer[countParts++].part = j;
		}
	}
#else
		vector <int> schedule;
		tuple <int, int> current;
		int nid, pid;
		int refer = 0;

		for(int i=0; i<graph->num_nodes; i++)
		{
			if(outDegree[i] % Part_Size == 0)
				thisNumParts = outDegree[i] / Part_Size;
			else
				thisNumParts = outDegree[i] / Part_Size + 1;
			
			refer += thisNumParts;
			schedule.push_back(thisNumParts - 1);
		}
		// std::cout << "parts: " << numParts << " refer: " << refer << " schedule.size(): " << schedule.size() <<  std::endl;
		int num_nodes = graph->num_nodes;
		int tmp_parts = numParts;
		int nid_idx = 0;
		while (tmp_parts > 0)
		{	
			if (schedule[nid_idx] > -1){
				partNodePointer[countParts].node = nid_idx;
				partNodePointer[countParts++].part = schedule[nid_idx];
				schedule[nid_idx] -= 1;
				tmp_parts -= 1;
			}
			nid_idx = (nid_idx + 1) % num_nodes;		
		}
		// std::cout << "countParts " << countParts << std::endl;
#endif

}
