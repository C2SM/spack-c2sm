# Make spack envs work with COSMO

This work assumes that your spack instance is loaded via `. setup-env.sh`.

## **Tested Environments**

- [x] `cosmo-cpu.yaml`
- [x] `cosmo-gpu.yaml`

## Spack env workflow with `spack install`
```shell
spack env create cosmo-gpu cosmo-gpu.yaml
spacktivate -p cosmo-gpu # spack env activate -p cosmo-gpu
spack concretize
spack install --test=root
```

## Spack development workflow with `spack develop`

We follow the approach from the official [spack documentation on developer workflows](https://spack-tutorial.readthedocs.io/en/latest/tutorial_developer_workflows.html).

```shell
spack env create -d cosmo-gpu_dev cosmo-gpu.yaml
cd cosmo-gpu_dev
spacktivate -p .
```

Now, we use `spack install` to build the entire development tree:

```shell
spack install
```

Afterwards, we specify which package and version we want to work on.

```shell
spack develop cosmo-dycore@c2sm-features
```

This has now been added to our spack.yaml:
```shell
grep -3 develop: spack.yaml
```

Then, we have to re-concretize and re-build.

```shell
spack concretize -f
spack install
```

This rebuilds `cosmo-dycore` from its subdirectory. Now, we can make changes to `cosmo-dycore`
and re-build with `spack install`. To work on other packages of the spec, start again from
`spack develop <package>@<variant>`.

### TODOs

- [x] Figure how to make a dev-build inside an activate environment
- [x] Figure how to build two codes (from same codebase) inside an acvtivate environment
- [ ] Combine `cosmo-cpu.yaml` and `cosmo-gpu.yaml` and  into a single file


# Issues

## Problem when parsing spec-string second time

When parsing a string of a spec using `spack.cmd.parse_specs(str(cosmo_spec))[0]` or
in `test_cosmo.py` spack complains about duplicate specs.
A valid spec may contain a spec twice, but parsing it from a string is not possible.
As a solution I suggest to change in installcosmo from
`cosmo_spec = spack.cmd.parse_specs(str(cosmo_spec))[0]` to `cosmo_spec = Spec.from_yaml(cosmo_spec.to_yaml())`.
This change is already done!

In the spack package we need to write the spec to a yaml-file as follows:
```python
with open('spec.yaml', mode='w') as f:
  f.write(self.spec.to_yaml()
```
This spec.yaml is passed as an argument to `test_cosmo.py` and create a spec-object as follows:
```python
with open('spec.yaml',"r") as f:
  Spec.from_yaml(f)
```
