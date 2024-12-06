from spack import *
from spack.pkg.builtin.icon import Icon as SpackIcon


class IconHam(SpackIcon):

    maintainers('stelliom')

    @run_before('build')
    def generate_hammoz_nml(self):
        with working_dir(self.configure_directory +
                         '/externals/atm_phy_echam_submodels/namelists'):
            make()

    def configure_args(self):
        args = super().configure_args()

        args.append('--enable-atm-phy-echam-submodels')
        args.append('--enable-hammoz')

        return args
