# Numba Survey

1.1. A ~5 minute guide to Numba — Numba 0.48.0-py3.6-macosx-10.7-x86_64.egg documentation
This seems to be a good read. 

Numba uses Just In Time compiler to take python code and produce machine code directly. 

However Numba only works with numpy and math heavy code. 

It uses python decorator to give JIT compilers hints on how to best compile for things. 

So numba probably won’t work with pytorch or tensorflow directly. Not to mention less main streamed deep graph library or pytorch geometry. 

7.2. A Map of the Numba Repository — Numba 0.48.0-py3.6-macosx-10.7-x86_64.egg documentation
This repomap of numba seems to be very useful and interesting. 
It touches upon bytecode, interprerator, runtime, type system, and CUDA gpu target. 

7.3. Numba architecture — Numba 0.48.0-py3.6-macosx-10.7-x86_64.egg documentation
Python bytecode to machine code example NUMBA.

7.6. Notes on Numba Runtime — Numba 0.48.0-py3.6-macosx-10.7-x86_64.egg documentation
Numba runtime note.NRT is a standalone C library with a Python binding. This allows NPM runtime feature to be used without the GIL. Currently, the only language feature implemented in NRT is memory management. (Maybe we can take a class concept and add it to NUMBA runtime--- look ahead compilation?? )

The plan for NRT is to make a standalone shared library that can be linked to Numba compiled code, including use within the Python interpreter and without the Python interpreter. To make that work, we will be doing some refactoring:
numba NPM code references statically compiled code in “helperlib.c”. Those functions should be moved to NRT.

7.8. Live Variable Analysis — Numba 0.48.0-py3.6-macosx-10.7-x86_64.egg documentation
Live variable analysis, somewhat related to garbage collection.

8. Numba Enhancement Proposals — Numba 0.48.0-py3.6-macosx-10.7-x86_64.egg documentation
Numba improvement proposal

8.2.2. NBEP 3: JIT Classes — Numba 0.48.0-py3.6-macosx-10.7-x86_64.egg documentation JIT classes features for numbda

8.2.4. NBEP 5: Type Inference — Numba 0.48.0-py3.6-macosx-10.7-x86_64.egg documentation NUMBA type inference


Accelerating Scientific Workloads with Numba - Siu Kwan Lam
Numba introduction video
Numba is good with numpy arrays and loops. 
Numba analyzes bytecode and emits machine code.

Numba - Tell Those C++ Bullies to Get Lost | SciPy 2017 Tutorial | Gil Forsyth & Lorena Barba
JIT for python. Not to replace Pypy or CPython
Specifically designed for math heavy python code.
Generates optimized machine code using LLLVM.
