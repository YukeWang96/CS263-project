ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.0-devel-ubuntu18.04
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION 7.6.0.64
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
            libcudnn7=$CUDNN_VERSION-1+cuda10.0 \
            libcudnn7-dev=$CUDNN_VERSION-1+cuda10.0 && \
    apt-mark hold libcudnn7 && \
    rm -rf /var/lib/apt/lists/*

# Env for CS263
RUN apt-get update &&  apt-get install -y \
    curl \
    ca-certificates \
    vim \
    sudo \
    git \
    bzip2 \
    libx11-6 \
    unzip \
    wget \
&& rm -rf /var/lib/apt/lists/*

# Create a working directory.
RUN mkdir /graphs
RUN mkdir /app
WORKDIR /app


# Create a non-root user and switch to it.
RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
 && chown -R user:user /app
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

# All users can use /home/user as their home directory.
ENV HOME=/home/user
RUN chmod 777 /home/user

# Install Miniconda.
# RUN wget \
#     https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
#     && mkdir /root/.conda \
#     && bash Miniconda3-latest-Linux-x86_64.sh -b \
#     && rm -f Miniconda3-latest-Linux-x86_64.sh 
# RUN conda --version

# RUN curl -so ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-4.5.12-Linux-x86_64.sh \
RUN curl -so ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
 && chmod +x ~/miniconda.sh \
 && ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh
ENV PATH=/home/user/miniconda/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false

# Create a Python 3.6 environment.
RUN /home/user/miniconda/bin/conda install conda-build \
 && /home/user/miniconda/bin/conda create -y --name py36 python=3.6.5 \
 && /home/user/miniconda/bin/conda clean -ya
ENV CONDA_DEFAULT_ENV=py36
ENV CONDA_PREFIX=/home/user/miniconda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:$PATH

# CUDA 10.0
RUN conda install pytorch==1.1.0 torchvision==0.3.0 cudatoolkit=10.0 -c pytorch

# Install HDF5 Python bindings.
RUN conda install -y h5py=2.8.0 \
 && conda clean -ya
RUN pip install h5py-cache==1.0

# Install Requests, a Python library for making HTTP requests.
RUN conda install -y requests=2.19.1 \
&& conda clean -ya

# Install Graphviz.
# RUN conda install -y graphviz=2.38.0 \
#  && conda clean -ya
RUN pip install graphviz==0.8.4
RUN conda install pandas=0.20.3

# Install OpenCV3 Python bindings.
RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    libgtk2.0-0 \
    libcanberra-gtk-module \
 && sudo rm -rf /var/lib/apt/lists/*
RUN conda install -y -c menpo opencv3=3.1.0 \
&& conda clean -ya

# Install PyTorch Geometric.
RUN CPATH=/usr/local/cuda/include:$CPATH \
 && LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH \
 && DYLD_LIBRARY_PATH=/usr/local/cuda/lib:$DYLD_LIBRARY_PATH

# no need for pytorch geometry for this env
# RUN pip install --verbose --no-cache-dir torch-scatter \
# && pip install --verbose --no-cache-dir torch-sparse \
# && pip install --verbose --no-cache-dir torch-cluster \
# && pip install --verbose --no-cache-dir torch-spline-conv \
# && pip install torch-geometric

RUN sudo apt-get update
RUN sudo apt-get install -y libsm6 libxext6 libxrender-dev
RUN pip install matplotlib \
 && pip install opencv-python \
 && pip install plyfile \
 && pip install 'networkx>=2.2,<2.3' \
 && pip install 'trimesh>=2.35.39,<2.35.40' \
 && pip install tensorflow==1.14 \
 && pip install pillow==6.1
# tensorflow for tensorboard support. CPU only. 

RUN sudo apt-get update
RUN sudo apt-get install -y build-essential
RUN sudo apt-get install -y g++