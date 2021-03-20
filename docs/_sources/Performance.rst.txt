Performance benchmarks of COSMO
===============================

The performance benchmarks is used to monitor and track performance changes to the
cosmo model. The plan fails if either the timing are 5% above the
reference, or if there is a change in the model output (check for bit identity).
The plan also checks if differences compare to the operational namelist have been made,
in which case it will issue a warning.

The performance benchmarks use a local git repository (no remote) to track changes.
When you make changes or update something, please create a commit so others can
see what you did. ``environment/perf-benchmarks`` uses a separate git repository with remotes.

Each testcase has a ``reference_float`` folder with reference files. This makes it possible
to check whether the current files are OK. ``reference_float`` should be kept up
to date when changes are made to testcases.

``TIMINGS_float.cfg`` defines the reference timings and thresholds. ``TOLERANCE_float``
defines the tolerance when checking the output values.

Because we have regularly issues with file access permissions, you should use
``fix_permissions.sh`` before and after you made changes.

Folders & Git repos:

* Performance benchmarks location: ``/project/g110/benchmarks/COSMO-ORG_performance_benchmark/``
* Results location: ``/project/g110/benchmarks/cosmo-org_benchmarks_results/``
* Jenkins plan: http://jenkins-mch.cscs.ch/view/cosmo/job/COSMO-ORG_performance_benchmark_daily/
* Git perf-benchmarks repo: https://github.com/C2SM-RCM/perf-benchmarks
