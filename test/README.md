# Unit tests
These tests are designed to run without a spack instance. They do not test spack. They do not test packages. They only test package descriptions or other stand-alone components.

# Integration tests
These tests are designed to test if spack-c2sm integrates with spack. They do not test packages.

# System tests
These tests are designed to test the collaboration of spack-c2sm, spack and the packages.

`icon_nwp_test.py` exercises the DACE fetch hook using the configured Spack
instance and local fetch scripts, without downloading or compiling ICON. Run it
with `spack python -m pytest -v test/icon_nwp_test.py` after activating the test
virtual environment and sourcing `setup-env.sh`. It covers in-source and
out-of-source layouts, existing checkouts, and recovery after an interrupted
fetch. These hook tests do not replace a full ICON build.
