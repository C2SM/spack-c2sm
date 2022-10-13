#!/bin/sh
# Prints the name of the machine this script runs on, or 'unknown'.

# /etc/xthostname exists on all CSCS machines except Tsa and Arolla
if test -f "/etc/xthostname"; then
    cat /etc/xthostname
else
    case $(hostname -s) in
        tsa*) echo tsa;;
        arolla*) echo arolla;;
        *) echo unknown;;
    esac
fi