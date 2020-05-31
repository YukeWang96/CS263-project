#include "gcn_sag.h"

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("gcn_sag", &gcn_sag);
}