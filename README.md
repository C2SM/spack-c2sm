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
| Load | `. spack-c2sm/setup-env.sh` autodetects machine <br>or<br>`. spack-c2sm/setup-env.sh <machine>` forces machine<br>or<br>`. spack-c2sm/setup-env.sh unknown` uses blank config<br>`spack compiler find` autodetects compilers<br>`spack external find --all` autodetects externally installed packages|
| Update | `git pull`<br>`git submodule update --recursive` |
| Clean | `spack uninstall -a` uninstalls all packages<br>`spack clean -a` cleans all misc caches<br>`rm -rf ~/.spack` removes user scope data |

**Spec syntax**: `<package> @<version> %<compiler> +<variant> ~<variant> ^<sub-package> +<sub-package-variant>`

|  | Command |
| --- | --- |
| Info | `spack info <package>` |
| Spec | `spack spec <spec>` concretizes abstract spec (unspecfied variant = **any**)<br>*Spack is not required to use the default of an unspecified variant. The default value is only a tiebreaker for the concretizer.* |
| Install  | `spack install <spec>` |
| Locate | `spack location --install-dir <spec>` prints location of **all** installs that satisfy the spec |
| Env | `spack load <spec>` loads run environment |
| Activate env | `spack env activate -p <env_name>` |
| Deactivate env | `spack deactivate` |

