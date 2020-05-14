[Python_C++_CUDA_Wrapper Pytorch, backed by Facebook, FAIR](https://pytorch.org/tutorials/advanced/cpp_extension.html)  
[Numba use example, bypassing C++ code, backed by NVIDIA](https://github.com/harrism/numba_examples/blob/master/mandelbrot_numba.ipynb)  
[PyCuDA, very similar to Numba](https://mathema.tician.de/software/pycuda/)  
[Scikit-cuda similar](https://github.com/lebedov/scikit-cuda)  

Wrapping our CUDA kernel into pytorch seems to be the most straightforward and close to metal wrapper. 

Numba, PyCuDA, Scikit-cuda all requres rewrite of the CUDA kernel we developed using python interface. 
