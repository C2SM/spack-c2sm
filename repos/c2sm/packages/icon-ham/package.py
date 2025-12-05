from spack import *
from spack.pkg.c2sm.icon import Icon as C2SMIcon
from collections import defaultdict


class IconHam(C2SMIcon):

    claw_values = ('std', 'validate')
    variant('claw',
            default='none',
            values=('none', ) + claw_values,
            description='Enable CLAW preprocessing')

    for x in claw_values:
        depends_on('claw', type='build', when='claw={0}'.format(x))

    conflicts('claw=validate', when='serialization=none')

    for x in claw_values:
        conflicts('+sct', when='claw={0}'.format(x))

    @run_before('build')
    def generate_hammoz_nml(self):
        with working_dir(self.configure_directory +
                         '/externals/hammoz/namelists'):
            make()

    def configure_args(self):
        args = super().configure_args()

        flags = defaultdict(list)

        claw = self.spec.variants['claw'].value
        if claw == 'none':
            args.append('--disable-claw')
        else:
            args.extend([
                '--enable-claw={0}'.format(claw),
                'CLAW={0}'.format(self.spec['claw'].prefix.bin.clawfc)
            ])
            flags['CLAWFLAGS'].append(
                self.spec['netcdf-fortran'].headers.include_flags)
            if '+cdi-pio' in self.spec:
                flags['CLAWFLAGS'].append(
                    self.spec['libcdi-pio'].headers.include_flags)

        if '+mpi' in self.spec:
            args.append('MPI_LAUNCH=false')

        args.append('--enable-atm-phy-echam-submodels')
        args.append('--enable-hammoz')

        args.extend([
            '{0}={1}'.format(var, ' '.join(val)) for var, val in flags.items()
        ])

        return args

    def build(self, spec, prefix):
        claw = self.spec.variants['claw'].value
        if claw != 'none' and make_jobs > 8:
            # Limit CLAW preprocessing to 8 parallel jobs to avoid
            # claw_f_lib.sh: fork: retry: Resource temporarily unavailable
            # ...
            # Error: Could not create the Java Virtual Machine.
            # Error: A fatal exception has occurred. Program will exit.
            make.jobs = 8
            make('preprocess')
            make.jobs = make_jobs
        make(*self.build_targets)
