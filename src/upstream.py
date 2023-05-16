import shutil
import sys
import os
import subprocess

sys.path.insert(1, 'spack/lib/spack/external')
from ruamel import yaml


def read_upstream_from_spack_yaml(config_dir):
    spack_yaml = os.path.join(config_dir, 'spack.yaml')
    with open(spack_yaml, 'r') as f:
        spack_config = yaml.load(f)
    upstream = spack_config['spack']['config']['install_tree']['root']
    return upstream


def delete_upstream(upstream):
    print(f'Delete upstream {upstream}')
    shutil.rmtree(upstream, ignore_errors=True)


def git_version():
    version = subprocess.check_output(
        "git --version", shell=True).decode().split('\n')[0].split(' ')[2]
    return int(version.replace(".", ""))


def current_tag():
    return subprocess.check_output("git describe --tags --abbrev=0",
                                   shell=True).decode().split('\n')[0]


def current_commit():
    return subprocess.check_output('git log -n 1 --pretty=format:"%H"',
                                   shell=True).decode().split('\n')[0]


def newer_tags(reference_tag):
    all_tags = subprocess.check_output("git tag --sort=authordate",
                                       shell=True).decode().split('\n')[0:-1]
    idx = all_tags.index(reference_tag)

    return all_tags[idx + 1:]


def upstream_from_another_tag(upstream_folder, tag):
    try:
        subprocess.check_output(
            f"git checkout {tag} {upstream_folder}",
            shell=True,
            stderr=subprocess.DEVNULL).decode().split('\n')[0:-1]
        upstream = read_upstream_from_spack_yaml(upstream_folder)
    except subprocess.CalledProcessError:
        upstream = None

    subprocess.check_output(f"git checkout {current_commit()} {upstream_folder}",
                            shell=True,
                            stderr=subprocess.DEVNULL)

    return upstream


if __name__ == '__main__':

    if len(sys.argv) != 2:
        raise ValueError('Need path to folder containing a spack.yaml')

    upstream = read_upstream_from_spack_yaml(sys.argv[1])
    upstream_is_still_in_use = False
    for tag in newer_tags(current_tag()):
        if upstream == upstream_from_another_tag(sys.argv[1], tag):
            upstream_is_still_in_use = True
            tag_using_upstream = tag
    if upstream_is_still_in_use:
        print(
            f'Can not delete upstream -> still in use for tag {tag_using_upstream}'
        )
    else:
        delete_upstream(upstream)
