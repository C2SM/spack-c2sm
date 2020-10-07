Hpc-container-maker: (https://github.com/NVIDIA/hpc-container-maker)

Use command:
  hpccm --recipe hpcbase-nvhpc-openmpi.py --format docker  --userarg cuda=10.1 ompi=4.0.2 centos=true nvhpc_eula_accept=yes >> Dockerfile
