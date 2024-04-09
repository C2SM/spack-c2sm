#!/bin/sh

ln -s /user-environment/config/compilers.yaml "$parent_dir"/sysconfigs/uenv/. 2> /dev/null
ln -s /user-environment/config/upstreams.yaml "$parent_dir"/sysconfigs/uenv/. 2> /dev/null
ln -s /user-environment/repo "$parent_dir"/repos/uenv 2> /dev/null
