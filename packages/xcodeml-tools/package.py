from spack import *
import os


class XcodemlTools(AutotoolsPackage):
    """Set of tools for translating C and Fortran code to XCodeML and back """

    homepage = 'https://omni-compiler.org/manual/en/'
    git = 'ssh://git@github.com/claw-project/xcodeml-tools.git'

    maintainers = ['FrostyMike']

    version('latest', branch='master')
    version('92a35f9',
            branch='master',
            commit='92a35f9dbe3601f6177b099825d318cbc3285945')

    depends_on('autoconf@2.69:')
    depends_on('m4')
    depends_on('automake')
    depends_on('libxml2')
    depends_on('java@8:')
    depends_on('bison')
    depends_on('flex')
    depends_on('libtool')

    def configure_args(self):
        args = [
            '--prefix=' + self.prefix, '--with-force-explicit-lxml2',
            '--without-native-fortran-compiler'
        ]
        libxml2_prefix = self.spec['libxml2'].prefix
        if libxml2_prefix == '/usr':
            args.append('--with-libxml2-include=/usr/include/libxml2')
            for lib_dir_name in ('lib', 'lib64'):
                lib_path = '/usr/%s/libxml2.so' % lib_dir_name
                if os.path.isfile(lib_path):
                    args.append('--with-libxml2-lib=/usr/%s' % lib_dir_name)
        else:
            args.append('--with-libxml2=' + libxml2_prefix)
        java_prefix = self.spec['java'].prefix
        path = {'java': 'bin/java', 'javac': 'bin/javac', 'jar': 'bin/jar'}
        for name, rel_path in path.items():
            abs_path = os.path.normpath(os.path.join(java_prefix, rel_path))
            assert os.path.exists(abs_path) and os.path.isfile(
                abs_path), '%s not found at "%s"' % (name, abs_path)
            path[name] = abs_path
        args.append('--with-java=' + path['java'])
        args.append('--with-javac=' + path['javac'])
        args.append('--with-jar=' + path['jar'])
        version_name = self.version
        version_tag = self.versions[version_name].get('commit', None)
        if version_tag is not None:
            args.append('--with-version-tag=' + version_tag)
        return args

    def setup_environment(self, spack_env, run_env):
        spack_env.set('YACC', 'bison -y')

    def setup_run_environment(self, run_env):
        java_prefix = self.spec['java'].prefix
        abs_path = os.path.normpath(os.path.join(java_prefix, 'bin/java'))
        assert os.path.exists(abs_path) and os.path.isfile(
            abs_path), 'java not found at "%s"' % abs_path
        run_env.set('OMNI_JAVA', abs_path)
