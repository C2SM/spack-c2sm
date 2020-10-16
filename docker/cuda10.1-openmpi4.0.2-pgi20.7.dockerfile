# 
# HPC Base image
# 
# Contents:
#   Mellanox OFED version 5.0-2.1.8.0
#   NVIDIA HPC SDK version 20.7
#   OpenMPI version 4.0.2
#   Python 2 and 3 (upstream)
# 

FROM nvidia/cuda:10.1-devel-centos8 AS devel

# Python
RUN yum install -y \
        python2 \
        python3 \
        python2-pip \
        git \
        openssh-server \
        json-c \
        lz4 \
        munge \
        ncurses \
        openssl \
        autoconf \
        automake \
        libtool \
        zlib \
        patch \
        mysql-devel && \
    rm -rf /var/cache/yum/*

# NVIDIA HPC SDK version 20.7
RUN yum install -y \
        gcc \
        gcc-c++ \
        gcc-gfortran \
        libatomic \
        numactl-libs \
        openssh-clients \
        wget \
        which && \
    rm -rf /var/cache/yum/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://developer.download.nvidia.com/hpc-sdk/nvhpc_2020_207_Linux_x86_64_cuda_multi.tar.gz && \
    mkdir -p /var/tmp && tar -x -f /var/tmp/nvhpc_2020_207_Linux_x86_64_cuda_multi.tar.gz -C /var/tmp -z && \
    cd /var/tmp/nvhpc_2020_207_Linux_x86_64_cuda_multi && NVHPC_ACCEPT_EULA=accept NVHPC_INSTALL_DIR=/opt/nvidia/hpc_sdk NVHPC_SILENT=true ./install && \
    rm -rf /var/tmp/nvhpc_2020_207_Linux_x86_64_cuda_multi /var/tmp/nvhpc_2020_207_Linux_x86_64_cuda_multi.tar.gz
ENV LD_LIBRARY_PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/20.7/comm_libs/nvshmem/lib:/opt/nvidia/hpc_sdk/Linux_x86_64/20.7/comm_libs/nccl/lib:/opt/nvidia/hpc_sdk/Linux_x86_64/20.7/math_libs/lib64:/opt/nvidia/hpc_sdk/Linux_x86_64/20.7/compilers/lib:/opt/nvidia/hpc_sdk/Linux_x86_64/20.7/cuda/lib64:$LD_LIBRARY_PATH \
    MANPATH=/opt/nvidia/hpc_sdk/Linux_x86_64/20.7/compilers/man:$MANPATH \
    PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/20.7/comm_libs/nvshmem/bin:/opt/nvidia/hpc_sdk/Linux_x86_64/20.7/comm_libs/nccl/bin:/opt/nvidia/hpc_sdk/Linux_x86_64/20.7/profilers/bin:/opt/nvidia/hpc_sdk/Linux_x86_64/20.7/compilers/bin:/opt/nvidia/hpc_sdk/Linux_x86_64/20.7/cuda/bin:$PATH

# Mellanox OFED version 5.0-2.1.8.0
RUN yum install -y \
        ca-certificates \
        gnupg \
        wget && \
    rm -rf /var/cache/yum/*
RUN rpm --import https://www.mellanox.com/downloads/ofed/RPM-GPG-KEY-Mellanox && \
    yum install -y dnf-utils && \
    yum-config-manager --add-repo https://linux.mellanox.com/public/repo/mlnx_ofed/5.0-2.1.8.0/rhel8.0/mellanox_mlnx_ofed.repo && \
    yum install -y \
        libibumad \
        libibverbs \
        libibverbs-utils \
        librdmacm \
        rdma-core \
        rdma-core-devel && \
    rm -rf /var/cache/yum/*

# OpenMPI version 4.0.2
RUN yum install -y \
        bzip2 \
        file \
        hwloc \
        make \
        numactl-devel \
        openssh-clients \
        perl \
        tar \
        wget && \
    rm -rf /var/cache/yum/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://www.open-mpi.org/software/ompi/v4.0/downloads/openmpi-4.0.2.tar.bz2 && \
    mkdir -p /var/tmp && tar -x -f /var/tmp/openmpi-4.0.2.tar.bz2 -C /var/tmp -j && \
    cd /var/tmp/openmpi-4.0.2 &&  CC=nvc CFLAGS=-O1 CXX=nvc++ F77=nvfortran F90=nvfortran FC=nvfortran FCFLAGS='-fpic -DPIC' ./configure --prefix=/usr/local/openmpi \
    --disable-getpwuid --enable-orterun-prefix-by-default --with-cuda=/opt/nvidia/hpc_sdk/Linux_x86_64/20.7/cuda --with-verbs && \
    make -j$(nproc) && \
    make -j$(nproc) install && \
    rm -rf /var/tmp/openmpi-4.0.2 /var/tmp/openmpi-4.0.2.tar.bz2
ENV LD_LIBRARY_PATH=/usr/local/openmpi/lib:$LD_LIBRARY_PATH \
    PATH=/usr/local/openmpi/bin:$PATH

ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    NVIDIA_REQUIRE_CUDA="cuda>=10.1 brand=tesla,driver>=384,driver<385 brand=tesla,driver>=396,driver<397 brand=tesla,driver>=410,driver<411" \
    NVIDIA_VISIBLE_DEVICES=all

ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    NVIDIA_REQUIRE_CUDA="cuda>=10.1 brand=tesla,driver>=384,driver<385 brand=tesla,driver>=396,driver<397 brand=tesla,driver>=410,driver<411" \
    NVIDIA_VISIBLE_DEVICES=all
