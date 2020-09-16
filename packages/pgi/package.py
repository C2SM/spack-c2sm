from spack import *
from spack.util.prefix import Prefix
import os

class Pgi(Package):
    """PGI optimizing multi-core x64 compilers for Linux, MacOS & Windows
    with support for debugging and profiling of local MPI processes.

    Note: This package cannot be installed, it wraps existing installation, specified 
    in packages.yaml.
    """
    homepage = "http://www.pgroup.com/"

    version('20.1', sha256='none')
    version('19.9', sha256='none')

    # Licensing
    license_required = True
    license_comment = '#'
    license_files = ['license.dat']
    license_vars = ['PGROUPD_LICENSE_FILE', 'LM_LICENSE_FILE']
    license_url = 'http://www.pgroup.com/doc/pgiinstall.pdf'
    
    def url_for_version(self, version):
        if int(str(version.up_to(1))) <= 17:
            return "file://{0}/pgilinux-20{1}-{2}-x86_64.tar.gz".format(
                os.getcwd(), version.up_to(1), version.joined)
        else:
            return "file://{0}/pgilinux-20{1}-{2}-x86-64.tar.gz".format(
                os.getcwd(), version.up_to(1), version.joined)

    def install(self, spec, prefix):
        pass

    def setup_run_environment(self, env):
        prefix = Prefix(join_path(self.prefix, 'linux86-64', self.version))

        env.prepend_path('PATH', prefix.bin)
        env.prepend_path('MANPATH', prefix.man)
        env.prepend_path('LD_LIBRARY_PATH', prefix.lib)
        env.set('CC',  join_path(prefix.bin, 'pgcc'))
        env.set('CXX', join_path(prefix.bin, 'pgc++'))
        env.set('F77', join_path(prefix.bin, 'pgfortran'))
        env.set('FC',  join_path(prefix.bin, 'pgfortran'))
