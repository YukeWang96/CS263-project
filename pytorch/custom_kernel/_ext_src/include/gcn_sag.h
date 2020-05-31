#pragma once
#include <torch/extension.h>

at::Tensor gcn_sag(
    at::Tensor nodePointer, // 1D
    at::Tensor edgeList, // 1D
    at::Tensor partNodePointer, // numNodes by 2
    at::Tensor embed_input, // 2D
    unsigned int numParts,
    unsigned int ebd_dim,
    unsigned int numNodes
);