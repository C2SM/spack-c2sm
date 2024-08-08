#!/bin/sh
# Prints the name of the machine this script runs on, or 'unknown'.

# /etc/xthostname exists on all CSCS machines
if test -f "/etc/xthostname"; then
    cat /etc/xthostname
else
    case $(hostname -s) in
        eu*) echo euler;;
        *) echo unknown;;
    esac
fi
