# Build stage with Spack pre-installed and ready to be used
FROM spack/centos7:0.15.3

ARG ssh_prv_key
ARG ssh_pub_key

COPY packages $SPACK_ROOT/packages
COPY repo.yaml $SPACK_ROOT
COPY sysconfigs/centos-7 $SPACK_ROOT/etc/spack

# Python 3
RUN yum update -y && \
    yum install -y \
    python3 \
    openssh-server \
    libmysqlclient-dev && \
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

RUN echo ". $SPACK_ROOT/share/spack/setup-env.sh" \
    > /etc/profile.d/spack.sh

# PGI compiler version 19.9

#RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -O /var/tmp/pgi-community-linux-x64-latest.tar.gz --referer https://www.pgroup.com/products/community.htm?utm_source=hpccm\&utm_medium=wgt\&utm_campaign=CE\&nvid=nv-int-14-39155 -P /var/tmp https://www.pgroup.com/support/downloader.php?file=pgi-community-linux-x64 && echo "DD" && \
#mkdir -p /var/tmp/pgi && tar -x -f /var/tmp/pgi-community-linux-x64-latest.tar.gz -C /var/tmp/pgi -z && echo "AA" && \
#cd /var/tmp/pgi && PGI_ACCEPT_EULA=accept PGI_INSTALL_DIR=/opt/pgi PGI_INSTALL_MPI=false PGI_INSTALL_NVIDIA=true PGI_MPI_GPU_SUPPORT=false PGI_SILENT=true ./install && echo "BB" && \
#echo "variable LIBRARY_PATH is environment(LIBRARY_PATH);" >> /opt/pgi/linux86-64/19.4/bin/siterc && \
#echo "variable library_path is default(\$if(\$LIBRARY_PATH,\$foreach(ll,\$replace(\$LIBRARY_PATH,":",), -L\$ll)));" >> /opt/pgi/linux86-64/19.4/bin/siterc && \
#echo "append LDLIBARGS=\$library_path;" >> /opt/pgi/linux86-64/19.4/bin/siterc && \
#rm -rf /var/tmp/pgi-community-linux-x64-latest.tar.gz /var/tmp/pgi

RUN spack install gcc@8.3.0 && spack compiler find

RUN spack install cosmo@master%gcc@8.3.0


LABEL "app"="cosmo"
LABEL "mpi"="openmpi"

ENTRYPOINT ["/bin/bash", "--rcfile", "/etc/profile", "-l"]
