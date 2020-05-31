// #include "../common/timer.hpp"
// #include "../common/tigr_utilities.hpp"
// #include "../common/graph.hpp"
// #include "../common/virtual_graph.hpp"
// #include "../common/globals.hpp"
// #include "../common/argument_parsing.hpp"
// #include "../common/gpu_error_check.cuh"

// #define using_shared
// #define CONTIOUS
// #define UNROLL
// #define PROF_DETAIL 
// #define DEBUG
// #define load_ebd_from_file

#include "gcn_sag.h"
#include "utils.h"


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
);

// pull-based aggregration with part-level sync and partial aggregration
at::Tensor gcn_sag(
    at::Tensor nodePointer, // 1D
    at::Tensor edgeList, // 1D
    at::Tensor partNodePointer, // numNodes by 2
    at::Tensor embed_input, // 2D, float, 1D, row_wise flattened // input
    unsigned int numParts,
    unsigned int ebd_dim,
    unsigned int numNodes
){
    CHECK_IS_FLOAT(embed_input);
    CHECK_IS_INT(partNodePointer);
    CHECK_IS_INT(nodePointer);
    CHECK_IS_INT(edgeList);

    at::Tensor output = torch::zeros({embed_input.size(0), embed_input.size(1)}, at::device(embed_input.device()).dtype(at::ScalarType::Float));

    gcn_sag_kernel_wrapper(
        numParts,
        nodePointer.data<int>(),
        ebd_dim,
        numNodes,
        partNodePointer.data<int>(),
        edgeList.data<int>(),
        edgeList.size(1), // length, num of edges
        output.data<float>(),
        embed_input.data<float>()
    );
    return output;
}