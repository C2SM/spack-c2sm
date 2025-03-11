Testing
=======

Test packages (PR/MR/CI/CD)
---------------------------

You can use spack to test a PR/MR in your CI pipeline.
This is a common way to do it.

.. code-block:: console

    # cd into the packages repo!
    $ git clone --depth 1 --recurse-submodules --shallow-submodules -b v0.20.1.0 https://github.com/C2SM/spack-c2sm.git
    $ . spack-c2sm/setup-env.sh
    $ spack dev-build --test=root --show-log-on-error <package> @develop <variant>

You can also use spack in your end-to-end tests.
This is a common way to do it.

.. code-block:: console

    $ spack install --test=root --show-log-on-error <package> @<version> <variant>

Pull Request Testing for spack-c2sm on GitHub
---------------------------------------------

To test a PR on Balfrin, post a comment ``launch jenkins``.
To test on Alps (Santis) post a comment ``cscs-ci run santis``.


Supported machines:

*   balfrin
*   santis

Jenkins test with uenv
----------------------
To test spack-c2sm with an uenv, add a stage

.. code-block:: bash

    stage('Create uenv') {
        steps {
            sh """
            git clone -b fix/jenkins https://github.com/eth-cscs/uenv.git
            ./uenv/install --yes --destdir=$WORKSPACE
            source $WORKSPACE/etc/profile.d/uenv.sh
            uenv repo create
            uenv image pull mch/v8:rc2
            """
        }
    }

and run the tests in the uenv

.. code-block:: bash

    source $WORKSPACE/etc/profile.d/uenv.sh
    source ./setup-env.sh /user-environment
    uenv run mch/v8:rc2 -- pytest -v -n auto test/integration_test.py
