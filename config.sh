#!/usr/bin/env bash

TEMP=$@
eval set -- "$TEMP --"
while true; do
    case "$1" in
        --idir|-i) install_dir=$2; shift 2;;
        --machine|-m) hostname=$2; shift 2;;
        --help|-h) help_enabled=yes; fwd_args="$fwd_args $1"; shift;;
        -- ) shift; break ;;
        * ) fwd_args="$fwd_args $1"; shift ;;
    esac
done

if [[ "${help_enabled}" == "yes" ]]; then
    echo "Available Options:"
    echo "* --help.  |-h {print help}"
    echo "* --machine|-m {machine name}     Required"
    echo "* --idir.  |-d {package dir}      Where the Spack instance will be installed. Default: \$(pwd)"
fi

if [[ -z ${install_dir} ]]; then
  install_dir=$PWD
fi

echo "Cloning spack instance to:" $install_dir

git clone git@github.com:spack/spack.git $install_dir/spack

echo "Installing mch packages &" $hostname "config files"

cp -rf $PWD/packages/* $install_dir/spack/var/spack/repos/builtin/packages

cp -rf $PWD/sysconfigs/$hostname/* $install_dir/spack/etc

echo "MCH Spack installed"

