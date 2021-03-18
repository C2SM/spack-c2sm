import os
import sys
import subprocess

from yamlconf import YamlConf


class BuildYamlConf(YamlConf):
    def __init__(self):
        cwd = os.getcwd()
        super().__init__(cwd+'/cosmo/ACC/jenkins/buildconf.yaml',
                         cwd+'/cosmo/ACC/jenkins/buildconf.schema')


class DepsYamlConf(YamlConf):
    def __init__(self, dir=None):
        if not dir:
            self.dir = os.getcwd()
        else:
            self.dir = dir
        super().__init__(self.dir+'/cosmo/ACC/dependencies.yaml',
                         self.dir+'/cosmo/ACC/dependencies.schema')

        check_tag = subprocess.run(
            ['git', 'describe', '--exact-match', '--tags', 'HEAD'], cwd=self.dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check_tag.returncode and self['version_from_git'] == 'true':
            cmd = 'git rev-parse --abbrev-ref HEAD'
            gitbranch = subprocess.run(
                cmd.split(), cwd=self.dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            self.git_tag_ = gitbranch.stdout.decode("utf-8").rstrip('\n')
        else:
            self.git_tag_ = check_tag.stdout.decode("utf-8").rstrip('\n')

    def dependency_spec(self, concretized_spec):

        eccodes_def_v = self['cosmo-eccodes-definitions']
        eccodes_v = self['eccodes']
        claw_v = self['claw']
        serialbox_v = self['serialbox']

        if self['version_from_git'] == 'true':
            tag = self.git_tag_
        else:
            tag = self["tag"]

        dycoredep = '^cosmo-dycore@'
        if self['version_from_git'] == 'true':
            dycoredep = dycoredep+tag
        else:
            dycoredep = dycoredep+self['cosmo-dycore']

        spack_spec = ''
        if concretized_spec.satisfies('+cppdycore'):
            spack_spec = spack_spec+' '+dycoredep
        if concretized_spec.satisfies('+eccodes'):
            spack_spec = spack_spec+' '+"^cosmo-eccodes-definitions@" + \
                eccodes_def_v + ' '+"^eccodes@"+eccodes_v
        if concretized_spec.satisfies('+claw'):
            spack_spec = spack_spec+' '+" ^claw@"+claw_v
        if concretized_spec.satisfies('+serialize'):
            spack_spec = spack_spec+' '+" ^serialbox@"+serialbox_v

        return spack_spec
