// #include "../common/timer.hpp"
// #include "../common/tigr_utilities.hpp"
// #include "../common/graph.hpp"
// #include "../common/virtual_graph.hpp"
// #include "../common/globals.hpp"
// #include "../common/argument_parsing.hpp"
// #include "../common/gpu_error_check.cuh"

#define OPT 3
// #define using_shared
// #define CONTIOUS
// #define UNROLL
// #define PROF_DETAIL 
// #define DEBUG
// #define load_ebd_from_file

#define MAX_EBD 5000
#define MAX_NB 10000
#define MAX_WK 1

#if OPT == 2
	#define thread_per_block 128
	#define point_per_block 128
#elif OPT == 3
	#define thread_per_block 1024 // 128
	#define point_per_block thread_per_block // 128
#endif

//@@@@@@@@@@@@@@ Optimization-2: push-based aggregration
#if OPT == 2
// Opt2: Push-based Aggregration reddit
__global__ void kernel(	
						unsigned int numParts, 
						unsigned int *nodePointer,
						unsigned int ebd_dim, 
						unsigned int numNodes,
						PartPointer *partNodePointer,
						unsigned int *edgeList,
						float *embed1,
						float *embed2
					)
{

	int partId = blockDim.x * blockIdx.x + threadIdx.x;
	
	if(partId < numParts)
	{

		__shared__ float currPt[MAX_EBD];
		int id = partNodePointer[partId].node;
		int part = partNodePointer[partId].part;

		// Opt1: caching current node
#ifdef UNROLL
		#pragma unroll
#endif
		for (int d = 0; d < ebd_dim; d++)
			currPt[d] = embed2[id * ebd_dim + d];

		int thisPointer = nodePointer[id];
		int degree = edgeList[thisPointer];
		int nid;
		int base = thisPointer + part * Part_Size + 1;

		// Opt3: caching neighbors idxs
		__shared__ unsigned int nb_ebd_idx[MAX_NB];

#ifdef UNROLL
			#pragma unroll
#endif
		for(int i = 0; i < Part_Size; i++)
		{
			if(i + part * Part_Size >= degree)
				break;

			nid = base + i;
			nb_ebd_idx[i] = edgeList[nid] * ebd_dim;

		}

		for(int i = 0; i < Part_Size; i++)
		{
			if(i + part * Part_Size >= degree)
				break;
#ifdef UNROLL
			#pragma unroll
#endif
			for (int d = 0; d < ebd_dim; d++)
				atomicAdd(&embed1[nb_ebd_idx[i] + d], currPt[d]);
		}
	}
}
#endif 

//@@@@@@@@@@@@@@ Optimization-3: pull-based aggregration
#if OPT == 3

#ifndef using_shared // no group leader selection
// pull-based aggregration with part-level sync and partial aggregration
__global__ void kernel(	
						unsigned int numParts, 
						unsigned int *nodePointer,
						unsigned int ebd_dim, 
						unsigned int numNodes,
						PartPointer *partNodePointer,
						unsigned int *edgeList,
						float *embed1,
						float *embed2
					)
{

	int partId = blockDim.x * blockIdx.x + threadIdx.x;
	
	// printf("partID: %d \n", partId);
	// printf("numParts: %d \n", numParts);

	if(partId < numParts)
	{

		// printf("partID: %d \n", partId);
		// printf("numParts: %d \n", numParts);

		float currPt[MAX_EBD];
		int id = partNodePointer[partId].node;
		int part = partNodePointer[partId].part;

		// Opt1: caching current node
		#ifdef UNROLL
			#pragma unroll
		#endif
			for (int d = 0; d < ebd_dim; d++)
				if (part == 0)
					currPt[d] = embed2[id * ebd_dim + d];
				else
					currPt[d] = 0;

		int thisPointer = nodePointer[id];
		int degree = edgeList[thisPointer];
		int nid;
		int thisNumParts;

		if(degree % Part_Size == 0)
			thisNumParts = degree / Part_Size ;
		else
			thisNumParts = degree / Part_Size + 1;

		#ifdef CONTIOUS
		int base = thisPointer + part * Part_Size + 1;
		#else
		int base = thisPointer + part + 1;
		#endif

		// Opt3: caching neighbors idxs
		__shared__ unsigned int nb_ebd_idx[MAX_NB];

		#ifdef UNROLL
			#pragma unroll
		#endif
		for(int i = 0; i < Part_Size; i++)
		{
			#ifdef CONTIOUS
				if(i + part * Part_Size >= degree) break;
				nid = base + i;
			#else
				// printf("%d\n", part + i * numParts);
				if(part + i * thisNumParts >= degree) break;
				nid = base + i * thisNumParts;
			#endif

			nb_ebd_idx[i] = edgeList[nid] * ebd_dim;
			// printf("partID: %d , %d, %d, %d\n", partId, id, nid, edgeList[nid]);
			for (int d = 0; d < ebd_dim; d++)
				currPt[d] += embed2[nb_ebd_idx[i] + d];
		}

		// for (int d = 0; d < ebd_dim; d++)
		// 	printf("%.3f ", currPt[d]);
		for (int d = 0; d < ebd_dim; d++)
			atomicAdd(&embed1[id * ebd_dim + d], currPt[d]);
	}
}
#endif

__global__ void Relu(float *matrix, int noOfElements){
    
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if(i < noOfElements)
        if (matrix[i] > 0)
            matrix[i] = matrix[i];
        else
            matrix[i] = 0;
}