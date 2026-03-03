#
#  Copyright (c) 2025, ETH Zurich. All rights reserved.
#
#  Please, refer to the LICENSE file in the root directory.
#  SPDX-License-Identifier: BSD-3-Clause
#


def create_batch_script(
    repo, num_nodes=1, account=None, custom_modules=None, branch="main", constraint=None
):
    script = f"""#!/bin/bash -l
#SBATCH --job-name="ci_job-spack-c2sm"
#SBATCH --output=job.out
#SBATCH --error=job.err
#SBATCH --time=0:50:00
#SBATCH --nodes={num_nodes}
"""

    if constraint:
        script += f"#SBATCH --constraint={constraint}\n"

    if account:
        script += f"#SBATCH --account={account}\n"

    script += f"""

# Clone command will fail if the directory already exists
# Remove this first if you are using the same working directory
# every time
if [ -d "firecrest-ci" ]; then
    rm -rf firecrest-ci
fi
git clone --depth 1 --shallow-submodules --recurse-submodules -b {branch} {repo} firecrest-ci
cd firecrest-ci

module use /mch-environment/v8/modules
module load python/3.11.7
"""

    if custom_modules:
        script += f"module load {' '.join(custom_modules)}\n"

    script += """
python -m venv testing-venv
source ./testing-venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements/test.txt
deactivate

python --version

source ./setup-env.sh
spack spec gnuconfig

source ./setup-env.sh /mch-environment/v8
source ./testing-venv/bin/activate
srun pytest -v -n 64 test/common_system_test.py test/balfrin_system_test.py
"""

    return script


def check_output(file_content):
    assert "loops, best of" in file_content
