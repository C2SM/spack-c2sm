# 
# HPC COSMO image
# 
# Contents:
#   CUDA version 10.0
#   HDF5 version 1.10.1
#   Mellanox OFED version 
#   OpenMPI version 3.0.0
#   PGI compilers version 19.4
#   Python 2 and 3 (upstream)
# 

FROM nvidia/cuda:10.0-devel-ubuntu18.04 AS devel
ARG nproc=2

# Python
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python \
        openssh-server \
        libmysqlclient-dev && \
        python3 && \
        rm -rf /var/lib/apt/lists/*

# Authorize SSH Host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts

# Add the keys and set permissions
RUN echo "$ssh_prv_key" > /root/.ssh/id_rsa && \
    echo "$ssh_pub_key" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

RUN mkdir /opt/spack && cd /opt/spack && git clone git@github.com:MeteoSwiss-APN/spack-mch.git && cd spack-mch && ./config.py -m ubuntu-18.04 -r spack/etc/spack -u OFF && . spack/share/spack/setup-env.sh

# PGI compiler version 19.4
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libnuma1 \
        perl \
        wget && \
    rm -rf /var/lib/apt/lists/*
RN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -O /var/tmp/pgi-community-linux-x64-latest.tar.gz --referer https://www.pgroup.com/products/community.htm?utm_source=hpccm\&utm_medium=wgt\&utm_campaign=CE\&nvid=nv-int-14-39155 -P /var/tmp https://www.pgroup.com/support/downloader.php?file=pgi-community-linux-x64 && echo "DD" && \
    mkdir -p /var/tmp/pgi && tar -x -f /var/tmp/pgi-community-linux-x64-latest.tar.gz -C /var/tmp/pgi -z && echo "AA" && \
    cd /var/tmp/pgi && PGI_ACCEPT_EULA=accept PGI_INSTALL_DIR=/opt/pgi PGI_INSTALL_MPI=false PGI_INSTALL_NVIDIA=true PGI_MPI_GPU_SUPPORT=false PGI_SILENT=true ./install && echo "BB" && \
    echo "variable LIBRARY_PATH is environment(LIBRARY_PATH);" >> /opt/pgi/linux86-64/19.4/bin/siterc && \
    echo "variable library_path is default(\$if(\$LIBRARY_PATH,\$foreach(ll,\$replace(\$LIBRARY_PATH,":",), -L\$ll)));" >> /opt/pgi/linux86-64/19.4/bin/siterc && \
    echo "append LDLIBARGS=\$library_path;" >> /opt/pgi/linux86-64/19.4/bin/siterc && \
    rm -rf /var/tmp/pgi-community-linux-x64-latest.tar.gz /var/tmp/pgi

ENV LD_LIBRARY_PATH=/opt/pgi/linux86-64/19.4/lib:$LD_LIBRARY_PATH \
    PATH=/opt/pgi/linux86-64/19.4/bin:$PATH

RUN spack compiler find && spack compiler list && spack install cosmo@master%pgi@19.4 ^openmpi+cuda

USER 666

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.0/compat/
ENV COSMO_HOME=/usr/local/cosmo
ENV PATH=$PATH:/usr/local/cosmo/cosmo/
WORKDIR /data
