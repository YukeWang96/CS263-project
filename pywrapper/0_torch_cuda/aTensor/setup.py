# from setuptools import setup, Extension
# from torch.utils import cpp_extension

# setup(name='lltm_cpp',
#       ext_modules=[cpp_extension.CppExtension('lltm_cpp', ['lltm.cpp'])],
#       cmdclass={'build_ext': cpp_extension.BuildExtension})

from torch.utils.cpp_extension import load

lltm_cpp = load(name="lltm_cpp", sources=["lltm.cpp"])