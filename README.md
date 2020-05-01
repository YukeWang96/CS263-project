# CS263-project
UCSB CS263 Project for Spring 2020 Quarter

# Member
* Yuke Wang
* Sirius Zhang

# Timeline 
- [x] **4/20** before 9am **[Project Vision Statement](https://docs.google.com/document/d/18AirkZSKz2w8TKl34t-w3aCTzGhYfbj87K1c0o_LhVQ/edit?usp=sharing)** Due (Initial Survey week)
- [x] **4/24** Github Friday 5 pm week 4 (**Survey week**, **document findings**, **further narrow down vision statement, decide on what to implement/code**)
- [x] **5/01**  Github Friday 5 pm week 5 (coding / implementation week 1)
- [ ] **5/08**  Github Friday 5 pm week 6 (coding / implementation week 2)
- [ ] **5/15** Github Friday 5 pm week 7 (coding / implementation week 3)
- [ ] **5/22** Github Friday 5 pm week 8 (profiling + Empirical evaluation, possibly across multiple frameworks week)
- [ ] **5/27** in class presentation (do we want to sign up for the 1 presentation day? Depending on our progress)
- [ ] **5/29** Github Friday 5 pm week 9 (Empirical evaluation + presentation preparation week)
- [ ] **6/01**  6/3 in class presentation dates
- [ ] **6/05**  Github Friday 5 pm week 10 (Documentation and report week)
- [ ] **6/08**  project report due


# Progress Logs
* **4/24**: 
> + Add 3 graph processing tools to `graph-tools/`, `prof_tools/`. 
> + Add `4-23-sv.md` to `surveys/`. 
> + Setup `Doxyfile` for `Doxygen`.

* **TODO**
> - [ ] numba survey
> - [ ] survey on different python profiling tools
> - [ ] survey and study on cuda profiling tools
> - [ ] create our own python graph library
> - [ ] decide the API names of our own python graph library
> - [ ] implement the sparse matrix multiply CPU-only implementation
> - [ ] implement the sparse matrix multiply GPU kernel
> - [ ] implement the scatter and gatther CPU-only implementation
> - [ ] implement the scatter and gatther GPU kernel
> - [ ] design the heuristic function on kernal switching

* **5/1**:
> + Add `0_el2csr.py` to convert plaintext edgelist graphs to CSR format stored as binary.
> + Add `4_metis.py`, `5_cluster_statis.py` and `6_gen_new_order-metis.py` to `graph-tools/` for graph clustering and node reordering. 
> + Node reordering aims to improve the cache performance and memory efficiency by assigning a set of nodes with strong interconnections (edges) with consecutive IDs (i.e. placing a a set of nodes within each cluster at continuous memory space).  



