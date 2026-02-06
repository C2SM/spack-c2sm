# The spack extension of C2SM and MCH
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://C2SM.github.io/spack-c2sm/latest)

Spack is the package manager used by C2SM and MeteoSwiss to install and deploy software on supercomputers, local machines and the cloud.

## Documentations

**Infos about c2sm-supported software and machines**
  * [spack-c2sm latest](https://C2SM.github.io/spack-c2sm/latest)
  * [spack-c2sm v0.20.1.4](https://C2SM.github.io/spack-c2sm/v0.20.1.4)
  * [spack-c2sm v0.20.1.3](https://C2SM.github.io/spack-c2sm/v0.20.1.3)
  * [spack-c2sm v0.20.1.0](https://C2SM.github.io/spack-c2sm/v0.20.1.0)
  * [spack-c2sm v0.18.x](https://C2SM.github.io/spack-c2sm/v0.18.1.12) [deprecated]

**General infos about spack**
  * [Official spack v0.21.1](https://spack.readthedocs.io/en/v0.21.1/)
  * [Official spack v0.20.1](https://spack.readthedocs.io/en/v0.20.1/)
  * [Official spack v0.18.1](https://spack.readthedocs.io/en/v0.18.1/) [deprecated]

The first 3 numbers of every spack-c2sm version match with the version of spack it uses as a submodule.

## Workflow for Users
We suggest local/individual spack instances and the use of spack environments.

Clone the repository
```bash
git clone --depth 1 --recurse-submodules --shallow-submodules -b v0.21.1.3 https://github.com/C2SM/spack-c2sm.git
```
Setup the shell environment and optionally specify an upstream, where spack will look for installed software, i.e.
```bash
. spack-c2sm/setup-env.sh
. spack-c2sm/setup-env.sh /user-environment
. spack-c2sm/setup-env.sh /mch-environment/v6
. spack-c2sm/setup-env.sh /mch-environment/v7
```
Sourcing this file will put the spack command in your PATH, set up your MODULEPATH to use Spack’s packages, and add other useful shell integration for certain commands, environments, and modules. For bash, it also sets up tab completion. (source: [spack docu](https://spack.readthedocs.io/en/v0.21.1/getting_started.html#shell-support))

Optionally activate a spack environment
```bash
spack env activate <path_to_env>
```
and starts exploring
```bash
spack info <package>
spack spec <spec>
```
and installing
```bash
spack install <spec>
spack dev-build <spec>
```
packages.

Updating spack-c2sm is in the hands of the user.
```bash
git pull
git submodule update --recursive
```
Before an update we advice to clean your instance
```bash
spack uninstall -a
spack clean -a
rm -rf ~/.spack
```
After an update we advice to rebuild packages, preferably in a new shell so that no outdated shell variables are retained.

## Workflow for Local Spack Development (Linting & Testing)

Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```
Install pinned dev tools
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
Install pre-commit hooks locally (optional)
```bash
pre-commit install
```
> Hooks run automatically on `git commit`

Run all hooks manually (recommended before push)
```bash
pre-commit run --all-files
```
> * Lints and auto-fixes safe issues (like unused imports)
> * Checks YAML, formatting, and other configured hooks
> * Shows errors/warnings for anything that cannot be auto-fixed

## Releases/Tags
Release tags are created by the Spack-Admin GitHub Team as needed or upon request.
The creation of a new release tag is coordinated within the admin team.

When creating a new release tag please follow the naming convention below:

```
v${SPACK_VERSION}.${SPACK_C2SM_VERSION}
```

Where `SPACK_VERSION` corresponds to the upstream Spack version this repo is based on, e.g. `SPACK_VERSION=0.22.2`. `SPACK_C2SM_VERSION` is the number of releases based on a specific `SPACK_VERSION`, starting from 0, which corresponds to the release adapting spack-c2sm to a new upstream Spack version. So, for example v0.22.2.5 is the fifth (sixth if you count the transitional release v0.22.2.0) spack-c2sm release based on Spack v0.22.2.

## Command cheat sheet
|  | Command |
| --- | --- |
| Clone | `git clone --depth 1 --recurse-submodules --shallow-submodules -b <branch/tag> https://github.com/C2SM/spack-c2sm.git` |
| Update | `git pull`<br>`git submodule update --recursive` |
| Load | `. spack-c2sm/setup-env.sh` to run without an upstream<br>or<br>`. spack-c2sm/setup-env.sh /user-environment` to use `/user-environment` as an upsream<br>`spack compiler find` [autodetects compilers](https://spack.readthedocs.io/en/v0.21.1/command_index.html?highlight=spack%20load#spack-compiler-find)<br>`spack external find --all` [autodetects externally installed packages](https://spack.readthedocs.io/en/v0.21.1/command_index.html?highlight=spack%20load#spack-external-find)|
| Clean | `spack uninstall -a` [uninstalls all packages](https://spack.readthedocs.io/en/v0.21.1/command_index.html?highlight=spack%20load#spack-uninstall)<br>`spack clean -a` [cleans all misc caches](https://spack.readthedocs.io/en/v0.21.1/command_index.html?highlight=spack%20load#spack-clean)|

[**Spec syntax**](https://spack.readthedocs.io/en/v0.21.1/basic_usage.html#specs-dependencies): `<package>`[`@<version>`](https://spack.readthedocs.io/en/v0.21.1/basic_usage.html#version-specifier)[`%<compiler>`](https://spack.readthedocs.io/en/v0.21.1/basic_usage.html#compiler-specifier)[`+<variant> ~<variant>`](https://spack.readthedocs.io/en/v0.21.1/basic_usage.html#variants)[`^<sub-package> +<sub-package-variant>`](https://spack.readthedocs.io/en/v0.21.1/basic_usage.html#specs-dependencies)[`<compiler flags>`](https://spack.readthedocs.io/en/v0.21.1/basic_usage.html#compiler-flags)

|  | Command |
| --- | --- |
| Find | `spack find` lists all installed packages. <br>`spack find <spec>` lists all installed packages that match the spec.
| Info | `spack info <package>` |
| Spec | `spack spec <spec>` concretizes abstract spec (unspecfied variant = **any**)<br>*Spack is not required to use the default of an unspecified variant. The default value is only a tiebreaker for the concretizer.* |
| Install  | `spack install <spec>` |
| Locate | `spack location --install-dir <spec>` prints location of **all** installs that satisfy the spec |
| [Load env](https://spack.readthedocs.io/en/v0.21.1/command_index.html?highlight=spack%20load#spack-load) | `spack load <spec>` loads run environment |
| [Activate env](https://spack.readthedocs.io/en/v0.21.1/environments.html) | `spack env activate <env_name>` |
| [Deactivate env](https://spack.readthedocs.io/en/v0.21.1/environments.html) | `spack deactivate` |
