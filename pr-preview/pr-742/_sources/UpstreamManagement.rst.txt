Upstream management
=====================================
spack-c2sm is aware of multiple upstream instances
providing pre-built dependencies. This is important for efficient builds during CI.
Additionally an overload of filesystems at CSCS is prevented because not every users install
its own software stack.

Install upstream
----------------------
The upstream instances are installed for each tag through a dedicated `Jenkinks plan (Install upstream) <https://jenkins-mch.cscs.ch/job/Spack/job/spack-upstream_v0.20.1.0/>`_.
Each new tag of spack-c2sm needs a new plan, it can simply be copied from existing one. The only thing to adapt is the default value of the spack-tag.

Uninstall upstream
----------------------
The upstream instances are uninstalled for each tag through a common `Jenkinks plan (Uninstall upstream) <https://jenkins-mch.cscs.ch/job/Spack/job/spack-delete-upstream/>`_ . No manual deletion of files in g110 needed.
In case multiple tags of spack-c2sm use the same version of an upstream a mechanism is programmed that checks if a given upstream is still used for future releases.
In that case the upstream is not removed.

..  attention::
    Automatic deinstallation of upstreams is only implemented in spack-c2sm v0.18.1.4 and later! A check if an upstream is still in use in later releases is in place v0.18.1.6 and later.


.. figure:: pictures/upstream_scheme.png

   Installation scheme of upstream instances. If tag v0.18.0.5 is the oldest tag supported, the orange upstream instances can safely be removed.
