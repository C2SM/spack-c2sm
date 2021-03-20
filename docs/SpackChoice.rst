Why was spack chosen by MeteoSwiss?
===================================

So the question came up why spack was chosen as the package manager for MeteoSwiss
and I wanted to try to answer this here so that others can see this as well
(my account may be incomplete, but should hopefully give a decent view on the whole topic):

The main issue is that MCH has some hefty requirements when it comes to building software.

To just name a few:

* We need to be able to build multiple versions and configurations of the same software
  (most linux distributions will provide one officially supported version and for others
  you're mostly on your own)
* Hardware matters for our software due to performance reasons. E.g., the MPI implementation
  or specific GPU models are important (this is a problem for package managers that try
  to create very isolated build environments)
* Build Systems of some of our software can be quite tricky to deal with (as part of
  its build process COSMO requires one to edit the Makefile which we usually automate
  with something like regex I believe)
* We often have to build a lot of HPC dependencies/libraries that aren't part of a
  usual system's installation (which means we don't really want to just use some bash
  scripts, we tried that and it became very difficult to maintain)
* We want to also create development builds and possibly hack the build of a package
  (clean building of packages isn't enough, we also need hackability)
* We have multiple relevant machines all with different hardware, MPI implementations
  and Accelerators/GPUs  (MCH alone needs tsa & daint, but we used to also have kesch
  and our collaborators have a whole lot of other machines as well)

These requirements are very common in HPC and they rule out a lot of popular solutions
(e.g., `apt-get`, `pacman`, `rpm`, etc). There are still quite a few package managers left
that could fullfill all the requirements. But of all of those spack has by far the
biggest adoption within HPC (just google "HPC package manager" and the first few pages
are dominated by spack).

Spack is adopted by:

* The US Department of Energy (which includes Aurora (1 exaFLOPS), Frontier
  (1.5 exaFLOPS) and El Capitan (2 exaFLOPS))
* Riken (this includes Fugaku (~2 exaFLOPS))
* CERN
* EPFL
* Fermilab
* CSCS provides some support for spack
  ( https://user.cscs.ch/computing/compilation/spack/ )

This strong dominance sets it apart from all other viable options. It only makes
sense for MCH to follow the rest of the industry.

A comparison of various tools (including spack) can be found
`here <https://easybuilders.github.io/easybuild-tutorial/comparison_other_tools/>`_
and
`here <https://archive.fosdem.org/2018/schedule/event/installing_software_for_scientists/attachments/slides/2437/export/events/attachments/installing_software_for_scientists/slides/2437/20180204_installing_software_for_scientists.pdf>`_.

I believe the timeline of spack at MCH was roughly:

* Sometime 2018 Valentin and Hannes gave a presentation about spack at MCH
* Summer 2019 an evaluation of possible solutions was done and it was determined
  that spack was the best option (probably same or similar reasons as above)
* November 2019 Elsa started her build & devops internship and until November 2020
  most software builds at MCH were ported to spack
* September/October/November 2020 was when most of the migration happened

Of course we regularly have issues with spack and these issues are time consuming
and frustrating. However, building, package management & dependencies is a very very
hard problem. While we regularly encounter bugs in spack and spack is still far away
from an optimal solution, there are also unavoidable issues when it comes to building
HPC software. You can't expect spack to solve unsolvable issues. Spack is only a tool.
If you misuse your tool, it's not fair to blame the tool for issues. Because spack
is trying to solve a complex problem, it also contains quite a bit of complexity
itself. If you're not willing to learn spack and ensure you're using it right,
you will have a bad time. But you will also have a bad time with any other solution
in this case. The idea that there is a magical tool that will automatically make
all our build requirements work is unfortunately not realistic at this point.
There are good reasons why there are so many package managers and users still
regularly encounter issues with them.
