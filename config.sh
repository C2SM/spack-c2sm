#!/usr/bin/env bash
version="v0.14.0"

TEMP=$@
eval set -- "$TEMP --"
while true; do
    case "$1" in
        --idir|-i) install_dir=$2; shift 2;;
        --machine|-m) hostname=$2; shift 2;;
        --version|-v) version=$2; shift 2;;
        --reposdir|-r) reposdir=$2; shift 2;;
        --help|-h) help_enabled=yes; fwd_args="$fwd_args $1"; shift;;
        -- ) shift; break ;;
        * ) fwd_args="$fwd_args $1"; shift ;;
    esac
done

if [[ "${help_enabled}" == "yes" ]]; then
    echo "Available Options:"
    echo "* --help.  |-h {print help}"
    echo "* --machine|-m {machine name}     Required"
    echo "* --version|-v {spack version}     Default: v0.14.0"
    echo "* --idir.  |-i {install dir}      Where the Spack instance is installed or you want it to be installed. Default: \$(pwd)"
fi

if [[ -z ${install_dir} ]]; then
  install_dir=$PWD
fi

if [[ ! -d "${install_dir}/spack" ]]; then
    echo "Cloning spack instance to:" $install_dir
    git clone git@github.com:spack/spack.git -b $version $install_dir/spack
fi

echo "Installing mch packages &" $hostname "config files"

if [[ -n ${reposdir} ]] && [[ ! -f "${reposdir}/repos.yaml" ]]; then
    echo " - $PWD" >> repos.yaml
    cp repos.yaml $reposdir/
fi

cp -rf $PWD/sysconfigs/$hostname/* $install_dir/spack/etc/spack

echo "MCH Spack installed"

