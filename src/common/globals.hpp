#ifndef GLOBALS_HPP
#define GLOBALS_HPP

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
#include <stdexcept>
#include <iostream>
#include <sstream> 

using namespace std;

typedef unsigned int uint;
const unsigned int Part_Size = 4;
const unsigned int DIST_INFINITY = std::numeric_limits<unsigned int>::max() - 1;

struct Edge{
    unsigned int source;
    unsigned int end;
};

struct Embedding{
    vector<float> embed; 
};


struct PartPointer{
	unsigned int node;
	unsigned int part;
    unsigned int node_shared_addr; // shared memory address id for common node
    bool group_leader=false;
};


#endif 	//	GLOBALS_HPP
