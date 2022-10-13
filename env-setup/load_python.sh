#!/bin/sh

case $1 in
    manali*|balfrin*) module load python/3.9.13-11.3.0-bteihqu;;
    daint*|dom*) module load cray-python;;
    tsa*|arolla*) module load python;;
esac