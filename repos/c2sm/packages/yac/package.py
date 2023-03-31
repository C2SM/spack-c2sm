from spack.util.environment import is_system_path


class Yac(AutotoolsPackage):
    """Yet another coupler: coupling ICON component models."""

    homepage = 'https://dkrz-sw.gitlab-pages.dkrz.de/yac/'
    url = 'https://gitlab.dkrz.de/dkrz-sw/yac'
    git = 'git@gitlab.dkrz.de:dkrz-sw/yac.git'

    version('2.1.1', tag='v2.1.1')
    version('1.5.5', tag='v1.5.5', preferred=True)
    version('1.5.4', tag='v1.5.4')

    variant('lib-only',
            default=True,
            description='omit building examples and utility programs')
    variant('xml', default=True, description='enable XML parsing')
    variant('netcdf', default=True, description='enable NetCDF support')
    variant('mpi', default=True, description='enable MPI support')
    variant('external-mtime',
            default=True,
            description='Use external mtime library')
    variant('lapack',
            default='lapacke',
            values=('mkl', 'lapacke', 'atlas', 'clapack', 'fortran',
                    'embedded'),
            description='Specify LAPACK backend')

    depends_on('libxml2', when='+xml')
    depends_on('netcdf-c', when='+netcdf')
    depends_on('mpi', when='+mpi')

    depends_on('yaxt@0.8.1:', when='@2:')

    depends_on('libmtime', when='+external-mtime')

    depends_on('mkl', when='lapack=mkl')
    depends_on('lapack', when='lapack=lapacke')
    depends_on('atlas', when='lapack=atlas')
    depends_on('clapack', when='lapack=clapack')
    depends_on('lapack', when='lapack=fortran')

    conflicts('^mkl',
              when='lapack=lapacke',
              msg='specify lapack=mkl if you want to build with MKL library')

    conflicts('^atlas',
              when='lapack=lapacke',
              msg='specify lapack=atlas if you want to build with ATLAS '
              'library')

    conflicts('~mpi',
              when='@2:',
              msg='YAC 2 cannot be built without MPI support')

    @property
    def libs(self):
        libraries = ['libyac']

        if self.spec.variants['lapack'].value == 'embedded':
            libraries.append('libyac_clapack')

        if '~external-mtime' in self.spec:
            libraries.append('libyac_mtime')

        return find_libraries(libraries,
                              root=self.prefix,
                              shared=False,
                              recursive=True)

    def configure_args(self):
        args = self.enable_or_disable('lib-only')
        args += self.enable_or_disable('netcdf')
        args += self.with_or_without('external-mtime')

        if '+xml' in self.spec:
            args.append('--enable-xml')

            # Account for the case when libxml2 is an external package installed
            # to a system directory, which means that Spack will not inject the
            # required -I flag with the compiler wrapper:
            xml2_spec = self.spec['libxml2']
            if is_system_path(xml2_spec.prefix):
                xml2_headers = xml2_spec.headers
                # We, however, should filter the pure system directories out:
                xml2_headers.directories = [
                    d for d in xml2_headers.directories
                    if not is_system_path(d)
                ]
                args.append('XML2_CFLAGS={0}'.format(xml2_headers.cpp_flags))
        else:
            args.append('--disable-xml')

        if '+mpi' in self.spec:
            if self.spec.satisfies('@:1'):
                # YAC 2 does not have the option:
                args.append('--enable-mpi')
            args.extend([
                'CC=' + self.spec['mpi'].mpicc,
                'FC=' + self.spec['mpi'].mpifc,
                # We cannot provide a universal value for MPI_LAUNCH,
                # therefore we have to disable the MPI checks:
                '--disable-mpi-checks'
            ])
        else:
            args.append('--disable-mpi')

        lapack = self.spec.variants['lapack'].value
        if lapack == 'embedded':
            args.append('--without-external-lapack')
        else:
            args.append('--with-external-lapack=' + lapack)
            if lapack == 'mkl':
                # Request LAPACK libraries from MKL:
                args.append('MKL_CLIBS=%s' %
                            self.spec['lapack:c'].libs.ld_flags)
            elif lapack == 'lapacke':
                args.append('LAPACKE_CLIBS=%s' %
                            self.spec['lapack:c'].libs.ld_flags)
            elif lapack == 'atlas':
                args.append('ATLAS_CLIBS=%s' %
                            self.spec['atlas'].libs.ld_flags)
            elif lapack == 'clapack':
                clapack_spec = self.spec['clapack']
                clapack_misnamed_libs = ['lapack_LINUX']
                clapack_libs = LibraryList([])
                if '+external-blas' in clapack_spec:
                    clapack_libs += find_libraries('libcblaswr',
                                                   clapack_spec.prefix,
                                                   shared=False)
                    clapack_libs += self.spec['atlas'].libs
                else:
                    clapack_misnamed_libs.append('blas_LINUX')
                clapack_libs += find_libraries('libf2c',
                                               clapack_spec.prefix.F2CLIBS,
                                               shared=False)
                args.extend([
                    'CLAPACK_CFLAGS=-I%s' % clapack_spec.prefix.INCLUDE,
                    'CLAPACK_CLIBS=%s %s' % (' '.join([
                        clapack_spec.prefix.join(lib + '.a')
                        for lib in clapack_misnamed_libs
                    ]), clapack_libs.ld_flags)
                ])
            elif lapack == 'fortran':
                args.append('FORTRAN_LAPACK_CLIBS=%s' %
                            self.spec['lapack:fortran'].libs.ld_flags)

        if self.run_tests and '^openmpi' in self.spec:
            args.append('MPI_LAUNCH=mpirun --oversubscribe')

        return args
