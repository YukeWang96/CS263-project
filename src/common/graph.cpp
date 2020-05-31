
#include "graph.hpp"


Graph::Graph(string graphFilePath, string graphEmbdPath, bool isWeighted)
{
	this->graphFilePath = graphFilePath;
	this->graphEmbdPath = graphEmbdPath;
	this->isWeighted = isWeighted;
	graphLoaded = false;
	hasZeroID = false;
}


void Graph::ReadGraph()
{
	cout << "Reading the input graph from the following file:\n>> " << graphFilePath << endl;
		
	ifstream infile;
	infile.open(graphFilePath);
	
	stringstream ss;
	
	uint max = 0;

	if(graphLoaded == true)
	{
		edges.clear();
		weights.clear();
	}	
	
	graphLoaded = true;
	
	uint source;
	uint end;
	uint w8;
	uint i = 0;
	
	string line;
	
	Edge newEdge;
	
	unsigned long edgeCounter = 0;
	
	while(getline( infile, line ))
	{
		if(line[0] < '0' || line[0] > '9')
			continue;
			
		ss.str("");
		ss.clear();
		ss << line;
		
		ss >> newEdge.source;
		ss >> newEdge.end;
		
		edges.push_back(newEdge);
		
		if (newEdge.source == 0)
			hasZeroID = true;
		if (newEdge.end == 0)
			hasZeroID = true;			
		if(max < newEdge.source)
			max = newEdge.source;
		if(max < newEdge.end)
			max = newEdge.end;
		
		if (isWeighted)
		{
			if (ss >> w8)
				weights.push_back(w8);
			else
				weights.push_back(1);
		}
		
		edgeCounter++;
	}
	
	infile.close();
	
	graphLoaded = true;
	
	num_edges = edgeCounter;
	num_nodes = max;
	if (hasZeroID)
		num_nodes++;
		
	cout << "==> Done reading Graph Edges.\n";
	cout << "Number of nodes = " << num_nodes << endl;
	cout << "Number of edges = " << num_edges << endl;
}

void Graph::ReadEmbedding(){
	cout << "Reading the input graph embedding from the following file:\n>> " << graphEmbdPath << endl;

	std::ifstream ifs(graphEmbdPath.c_str());
	std::string s;
	for (unsigned int i=0; i < num_nodes; i++){
		Embedding eb;
		std::getline( ifs, s );
		std::istringstream iss(s);
		copy( std::istream_iterator<float>( iss ), std::istream_iterator<float>(), std::back_inserter(eb.embed));
		// for(unsigned int d=0; d < eb.embed.size();d++)
		// 	std::cout << eb.embed[d] << " ";
		// std::cout << std::endl;
		pt_embeds.push_back(eb);
//      std::cout << "pid[" << i << "]= ("<< p.point << ")" <<std::endl;
	}
	std::cout << "==> Done Reading Node Embedding" << std::endl;
}