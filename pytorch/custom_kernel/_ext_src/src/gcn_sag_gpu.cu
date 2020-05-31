#include "cuda_utils.h"

#define MAX_EBD 5000
#define MAX_NB 10000
#define MAX_WK 1
#define Part_Size 1

#define thread_per_block 1024 // 128
#define point_per_block thread_per_block // 128

// pull-based aggregration with part-level sync and partial aggregration
__global__ void gcn_sag_forward_cuda(
    unsigned int numParts,
    int *nodePointer, // needs to be int * instead of unsigned int. undefined symbol bug otherwise.
    unsigned int ebd_dim,
    unsigned int numNodes,
    int *partNodePointer,
    int *edgeList,
    float *embed1,
    float *embed2
){
    int partId = blockDim.x * blockIdx.x + threadIdx.x;

    // printf("partID: %d \n", partId);
    // printf("numParts: %d \n", numParts);

    if(partId < numParts)
    {
        // printf("partID: %d \n", partId);
        // printf("numParts: %d \n", numParts);

        float currPt[MAX_EBD];
        int id = partNodePointer[partId*2+0]; // node idx
        int part = partNodePointer[partId*2+1]; // node part

        // Opt1: caching current node
        // #ifdef UNROLL
        // 	#pragma unroll
        // #endif
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

        // #ifdef CONTIOUS
        // int base = thisPointer + part * Part_Size + 1;
        // #else
        int base = thisPointer + part + 1;
        // #endif

        // Opt3: caching neighbors idxs
        unsigned int nb_ebd_idx[MAX_NB];

        // #ifdef UNROLL
        //  #pragma unroll
        // #endif
        for(int i = 0; i < Part_Size; i++)
        {
            // #ifdef CONTIOUS
            //  if(i + part * Part_Size >= degree) break;
            //  nid = base + i;
            // #else
            // printf("%d\n", part + i * numParts);
            if(part + i * thisNumParts >= degree) break;
            nid = base + i * thisNumParts;
            // #endif

            nb_ebd_idx[i] = edgeList[nid] * ebd_dim;
            // printf("partID: %d , %d, %d, %d\n", partId, id, nid, edgeList[nid]);
            for (int d = 0; d < ebd_dim; d++)
                currPt[d] += embed2[nb_ebd_idx[i] + d];
        }

        // for (int d = 0; d < ebd_dim; d++)
        //  printf("%.3f ", currPt[d]);
        for (int d = 0; d < ebd_dim; d++)
            atomicAdd(&embed1[id * ebd_dim + d], currPt[d]);
    }
}

void gcn_sag_kernel_wrapper(
    unsigned int numParts,
    int *nodePointer,
    unsigned int ebd_dim,
    unsigned int numNodes,
    int *partNodePointer,
    int *edgeList,
    unsigned int num_of_edges,
    float *embed1, // output
    float *embed2 // input
) {
    cudaStream_t stream = at::cuda::getCurrentCUDAStream();
    gcn_sag_forward_cuda<<<num_of_edges, 1024, 0, stream>>>(numParts, nodePointer, ebd_dim, numNodes, partNodePointer, edgeList, embed1, embed2);
    CUDA_CHECK_ERRORS();
}