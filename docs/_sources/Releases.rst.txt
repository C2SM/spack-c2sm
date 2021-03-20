Releases
===========

mch branch of MeteoSwiss-APN fork
-----------------------------------

The source code for preparing the COSMO releases is always at the `mch` branch of the fork in 
`<https://github.com/MeteoSwiss-APN/cosmo>`_


The git history of the `mch` branch is exactly the same as the COSMO-ORG upstream 
`<https://github.com/COSMO-ORG/cosmo>`_ except for the last commit with log "APPLY MCH CHANGES".
This last commit contains all the mch modifications required on top of the official COSMO code to create a MeteoSwiss executable. 


How to synchronize the mch branch with COSMO-ORG
--------------------------------------------------

Create a branch where to merge the head of COSMO-ORG

.. code-block:: bash
  
  git clone git@github.com:MeteoSwiss-APN/cosmo
  cd cosmo
  git remote add upstream git@github.com:COSMO-ORG/cosmo
  git checkout -b merge_branch
  git merge upstream/master


After resolving all the conflicts, force push the COSMO-ORG history into the MeteoSwiss-APN/cosmo fork

.. code-block:: bash

  git checkout -b master upstream/master
  git branch -D mch
  git checkout -b mch
  git push --force -u origin mch 

Copy all the files of the merge_branch and push into mch with a single commit "APPLY MCH CHANGES" 


MeteoSwiss Releases
---------------------

The MeteoSwiss releases of cosmo, `<https://github.com/MeteoSwiss-APN/cosmo/releases>`_  follow the following versioning:

.. code-block:: console

  <cosmo-org version>.mch<version of update from cosmo-org>.p<patch version>

An example of such versioning is `5.07.mch1.0.p10 <https://github.com/MeteoSwiss-APN/cosmo/releases/tag/5.07.mch1.0.p10>`_.

The <cosmo-org version> is the latest of the COSMO-ORG releases, `<https://github.com/COSMO-ORG/cosmo/releases>`_ at the time 
when the MeteoSwiss release is created. 
The <version of update from cosmo-org> is an index, with format <major>.<minor>, that is increased with every synchronization of COSMO-ORG 
into the mch branch. The <major> number is incremented only if the results are not bit reproducible with respect to the previous release. 
The <patch version> is incremented with every patch applied to the previous release. Patches are bug fixes that are in process of being merge into 
COSMO-ORG/cosmo, or occasionally into MeteoSwiss-APN/cosmo. 

The release notes of each release should contain:

 * a description of all the patches applied
 * Changes with respect to the last <version of update from cosmo-org>
 * The date when the <version of update from cosmo-org> was updated from COSMO-ORG

.. warning:: Since every update from COSMO-ORG is performed as a force-push (equivalent to a rebase) all the releases created are disconnect from the main history of the mch branch. 
   That is why is particularly important to specify in the release notes the date of the last time the release was updated from COSMO-ORG
