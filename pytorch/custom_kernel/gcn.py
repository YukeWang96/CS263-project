import torch
from torch.autograd import Function
import torch.nn as nn
import sys

try:
    import builtins
except:
    import __builtin__ as builtins

try:
    import custom_kernel._ext as _ext
except ImportError:
    if not getattr(builtins, "__CUSTOM_KERNEL_SETUP__", False):
        raise ImportError(
        "Could not import custom_kernel._ext module.\n"
    )

class GCN_SAG(Function):
    @staticmethod
    def forward(ctx, nodePointer, edgeList, partNodePointer, embed_input, numParts, ebd_dim, numNodes):
        return _ext.gcn_sag(nodePointer, edgeList, partNodePointer, embed_input, numParts, ebd_dim, numNodes)
        # return _ext.gcn_sag(embed_input, numParts, ebd_dim, numNodes)
    @staticmethod
    def backward(ctx, grad_out):
        return None, None, None, None, None, None, None
