# The spack extension of C2SM and MCH
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://C2SM.github.io/spack-c2sm/)

Spack is the package manager used by C2SM and MeteoSwiss to install and deploy software on supercomputers, local machines and the cloud.

Documentations: [spack-C2SM](https://C2SM.github.io/spack-c2sm/), [spack](https://spack.readthedocs.io/en/v0.18.1/)

## Workflow
With spack v0.18 we suggest local/individual spack instances and the use of spack environments.

A user clones the spack repo
```bash
git clone --depth 1 --recurse-submodules --shallow-submodules -b dev_v0.18.1 https://github.com/C2SM/spack-c2sm.git
```
gets spack in the command line
```bash
. spack-c2sm/setup-env.sh
```
activates an environment
```bash
spack env activate -p <path_to_env>
```
and starts exploring
```bash
spack info <package>
spack spec <spec>
```
and building
```bash
spack install <spec>
spack dev-build <spec>
```
a package.

Updating spack-c2sm is in the hands of the user.
```bash
git pull
git submodule update --recursive
```
After an update we advice to clean
```bash
spack uninstall -a
spack clean -a
rm -rf ~/.spack
```
and rebuild.

## Command cheat sheet
|  | Command |
| --- | --- |
| Clone | `git clone --depth 1 --recurse-submodules --shallow-submodules -b dev_v0.18.1 https://github.com/C2SM/spack-c2sm.git` |
| Load | `. spack-c2sm/setup-env.sh` autodetects machine <br>or<br>`. spack-c2sm/setup-env.sh <machine>` forces machine<br>or<br>`. spack-c2sm/setup-env.sh unknown` uses blank config<br>`spack compiler find` [autodetects compilers](https://spack.readthedocs.io/en/v0.18.1/command_index.html?highlight=spack%20load#spack-compiler-find)<br>`spack external find --all` [autodetects externally installed packages](https://spack.readthedocs.io/en/v0.18.1/command_index.html?highlight=spack%20load#spack-external-find)|
| Update | `git pull`<br>`git submodule update --recursive` |
| Clean | `spack uninstall -a` [uninstalls all packages](https://spack.readthedocs.io/en/v0.18.1/command_index.html?highlight=spack%20load#spack-uninstall)<br>`spack clean -a` [cleans all misc caches](https://spack.readthedocs.io/en/v0.18.1/command_index.html?highlight=spack%20load#spack-clean)<br>`rm -rf ~/.spack` removes user scope data |

[**Spec syntax**](https://spack.readthedocs.io/en/v0.18.1/basic_usage.html#specs-dependencies): `<package>`[`@<version>`](https://spack.readthedocs.io/en/v0.18.1/basic_usage.html#version-specifier)[`%<compiler>`](https://spack.readthedocs.io/en/v0.18.1/basic_usage.html#compiler-specifier)[`+<variant> ~<variant>`](https://spack.readthedocs.io/en/v0.18.1/basic_usage.html#variants)[`^<sub-package> +<sub-package-variant>`](https://spack.readthedocs.io/en/v0.18.1/basic_usage.html#specs-dependencies)[`<compiler flags>`](https://spack.readthedocs.io/en/v0.18.1/basic_usage.html#compiler-flags)

|  | Command |
| --- | --- |
| Info | `spack info <package>` |
| Spec | `spack spec <spec>` concretizes abstract spec (unspecfied variant = **any**)<br>*Spack is not required to use the default of an unspecified variant. The default value is only a tiebreaker for the concretizer.* |
| Install  | `spack install <spec>` |
| Locate | `spack location --install-dir <spec>` prints location of **all** installs that satisfy the spec |
| [Load env](https://spack.readthedocs.io/en/v0.18.1/command_index.html?highlight=spack%20load#spack-load) | `spack load <spec>` loads run environment |
| [Activate env](https://spack.readthedocs.io/en/v0.18.1/environments.html) | `spack env activate -p <env_name>` |
| [Deactivate env](https://spack.readthedocs.io/en/v0.18.1/environments.html) | `spack deactivate` |

