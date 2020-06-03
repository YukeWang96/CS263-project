# CS263-Project
UCSB CS263 Project for Spring 2020 Quarter

# Member
* **Yuke Wang**
* **Sirius Zhang**

# Tutorial
## Directories and Files
**```cs263-project```**
> + ```Docker/```: The runtime environment Docker configuration file. <br>
> + ```graph-tools/```: Python scripts to process graph edge lists in plain text. <br>
> + ```prof-tools/```: Python scripts to generate profile report in **.csv** format. <br>
> + ```pytorch/```: the **major folder** contains the Pytorch-wrapped SAG kernel and SpMM.<br>
>> + ```custom_kernel/```: GPU kernel and Pytorch Wrapper src.
>>> + ```graph.py```:  graph definition and built-in functions.
>>> + ```main.py``` :  major driver for evalution GCN kernels.
>>> + ```model.py```:  GCN model definition.
>>> + ```virtual_graph.py```: group-based workload partitioning.
>>> + ```setup.py```: Pytorch Wrapper for GCN kernel.
>>> + ```test.py```: Test file for wrapper validation.
>> + ```prof-results/```: kernel profiling report in .csv format
>> + ```logs/```: profiling logs from NVProf.
> + ```pywrapper/```: Other alternative solutions for wrapping c/c++ source for Python.<br>
> + ```src/```: CUDA kernel source without Pytorch Wrapper. <br>
> + ```surveys/```: contains the initial surveys of this project. <br>

## Step-1
### Start Docker
> 1. ```cd pytorch/``` <br> 
> 2. ```cd Docker``` <br>
> 3. ```docker build -t cs263_project --build-arg IMAGE_NAME=nvidia/cuda . ```  <br>
> 4. ```docker run --rm -it --init --runtime=nvidia --ipc=host --name cs263_project --user=0 -v ~/CS263-project:/app -v [PATH-TO-GRAPH-FOLDER]:/graphs cs263_project``` <br>
<!-- >> + ```docker run --rm -it --init --runtime=nvidia --ipc=host --name cs263_project --user=0 -v ~/cs263-sirius:/app -v ~/.graphs/orig:/graphs cs263_project``` <br> -->
> 5. ```cd pytorch/custom_kernel``` <br>
> 6. ```python setup.py install``` <br>
> 7. ```python test.py # verify installation``` <br>

> **Note: command 3 only need to run if ```cs263_project``` has not been built before. Ohterwise, if ```cs263_project``` docker image already exists, just jump from 2 to 4.** 

## Step-2
### Standalone Mode -- Single Graph 
> * For running a single graph.
>> **```python custom_kernel/main.py```** <br>
>> ```--graph_path``` absolute path of GNN graph file in [coo format](https://scipy-lectures.org/advanced/scipy_sparse/coo_matrix.html) as **plain text** file. Note that node id must start from 0 and be continuous<br>
>> ```--feature``` size of feature embedding (default=100)<br>
>> ```--hidden``` size of hidden dimension of GNN network (default=16) <br>
>> ```--kernel``` GNN kernel: SAG (default), and SpMM <br>
>> ```--gpu:``` set if use GPU, otherwise CPU.

## Step-3
### Benchmark Mode -- Multiple Graphs 
> * For running several graphs.
>>  **```./run-bench.py```** <br>
>>  ```overall```: **True** if profile overall CUDA kernel runtime(fast), otherwise, profile kernel detailed metrics (slow). <br>
>> ```hidden```: dimension of GCN hidden layers.<br>
>> ```data_dir```: absolute path for the graph directory ```default="/graphs/"```

# Project Timeline 
- [x] **4/20** before 9am **[Project Vision Statement](https://docs.google.com/document/d/18AirkZSKz2w8TKl34t-w3aCTzGhYfbj87K1c0o_LhVQ/edit?usp=sharing)** Due (Initial Survey week)
- [x] **4/24** Github Friday 5 pm week 4 (**Survey week**, **document findings**, **further narrow down vision statement, decide on what to implement/code**)
- [x] **5/01**  Github Friday 5 pm week 5 (coding / implementation week 1)
- [x] **5/08**  Github Friday 5 pm week 6 (coding / implementation week 2)
- [x] **5/15** Github Friday 5 pm week 7 (coding / implementation week 3)
- [x] **5/22** Github Friday 5 pm week 8 (profiling + Empirical evaluation, possibly across multiple frameworks week)
- [x] **5/29** Github Friday 5 pm week 9 (Empirical evaluation + presentation preparation week)
- [ ] **6/03**  6/3 in class presentation dates
- [ ] **6/05**  Github Friday 5 pm week 10 (Documentation and report week)
- [ ] **6/08**  project report due

# Progress Logs
* **4/24**: 
> + Add 3 graph processing tools to `graph-tools/`, `prof_tools/`. 
> + Add `4-23-sv.md` to `surveys/`. 
> + Setup `Doxyfile` for `Doxygen`.

* **TODO**
> - [x] numba survey
> - [x] survey on different python profiling tools
> - [x] survey and study on cuda profiling tools
> - [x] create our own python graph library
> - [x] decide the API names of our own python graph library
> - [x] implement the sparse matrix multiply CPU-only implementation
> - [x] implement the sparse matrix multiply GPU kernel
> - [x] implement the scatter and gatther CPU-only implementation
> - [x] implement the scatter and gatther GPU kernel

* **5/1**:
> + Add `0_el2csr.py` to convert plaintext edgelist graphs to CSR format stored as binary.
> + Add `4_metis.py`, `5_cluster_statis.py` and `6_gen_new_order-metis.py` to `graph-tools/` for graph clustering and node reordering. 
> + Node reordering aims to improve the cache performance and memory efficiency by assigning a set of nodes with strong interconnections (edges) with consecutive IDs (i.e. placing a a set of nodes within each cluster at continuous memory space).  

* **5/8**:
> + Add `degree_stddev` to `prof-tools` for graph node degree statistics
> + Add `01_metrics.py` to `prof-tools` for CUDA-related detailed profiling
> + Add `02_memory_latency.py` to `prof-tools` for evaluting memory access overhead.

* **5/15**:
> + Add `graph.hpp` (**graph definition**) and `virtual_graph.hpp` (**group-based workload**) to `src/common`.
> + Add `gcn.cu` (**2-layer GCN**)and `gnn.hpp` (**aggregation kernel**) to `src/kernel`. 

* **5/22**:
> + Add `globals.hpp`, `graph.cpp` and `virtual_graph.cpp` for graph kernel implementation.
> + Add `Makefile` to `common` directory.
> + Finish the initial evaluation for GCN.

* **5/29**:
> + Add `gcn.cu` for SpMM-based GCN kernel.
> + Add `edgelist_to_csr` for graph-preprocessing tools.

* **5/31**:
> + Wrap the GCN kernel for Pytorch.
> + Add the Docker