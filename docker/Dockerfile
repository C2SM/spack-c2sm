# 
# HPC Base image
# 
# Contents:
#   Mellanox OFED version 5.0-2.1.8.0
#   NVIDIA HPC SDK version 20.7
#   OpenMPI version 4.0.2
#   Python 2 and 3 (upstream)
# 

FROM elsagermann/cuda10.1-openmpi4.0.2-pgi20.7:latest AS devel

ARG ssh_prv_key
ARG ssh_pub_key
ARG spack_spec=cosmo@master%pgi

# Authorize SSH Host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts

# Add the keys and set permissions
RUN echo "$ssh_prv_key" > /root/.ssh/id_rsa && \
    echo "$ssh_pub_key" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

RUN mkdir -p /opt/spack && cd /opt/spack && \
    git clone git@github.com:MeteoSwiss-APN/spack-mch.git -b docker && \
    cd spack-mch && pip2 install -U pip setuptools wheel && pip2 install pyyaml && \
    ./config.py -m centos-8 -p /opt/spack -r spack/etc/spack -u OFF && \
    . spack/share/spack/setup-env.sh && spack compiler find && \
    git clone git@github.com:jonasjucker/cosmo.git -b docker && \
    cd cosmo && spack dev-build $spack_spec

FROM nvidia/cuda:10.1-devel-centos8

# Python
RUN yum install -y \
        python2 \
        python3 && \
    rm -rf /var/cache/yum/*

# NVIDIA HPC SDK
RUN yum install -y \
        libatomic \
        numactl-libs \
        openssh-clients && \
    rm -rf /var/cache/yum/*
COPY --from=devel /opt/nvidia/hpc_sdk/Linux_x86_64/20.7/REDIST/compilers/lib/* /opt/nvidia/hpc_sdk/Linux_x86_64/20.7/compilers/lib/
ENV LD_LIBRARY_PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/20.7/compilers/lib:$LD_LIBRARY_PATH

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

# OpenMPI
RUN yum install -y \
        hwloc \
        openssh-clients && \
    rm -rf /var/cache/yum/*
COPY --from=devel /usr/local/openmpi /usr/local/openmpi
ENV LD_LIBRARY_PATH=/usr/local/openmpi/lib:$LD_LIBRARY_PATH \
    PATH=/usr/local/openmpi/bin:$PATH

# Cuda 
COPY --from=devel /usr/local/cuda /usr/local/cuda
ENV LD_LIBRARY_PATH=/usr/local/cuda/compat:$LD_LIBRARY_PATH \
    PATH=/usr/local/cuda/bin:$PATH

# Spack
COPY --from=devel /opt/spack /opt/spack
