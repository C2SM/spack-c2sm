from spack import *
from spack.pkg.c2sm.icon import Icon as C2SMIcon


class IconHam(C2SMIcon):

    variant('ham', default=True, description='Enable the hammoz submodel')

    @run_before('build')
    def generate_hammoz_nml(self):
        if '+ham' in self.spec:
            with working_dir('./externals/atm_phy_echam_submodels/namelists'):
                make()

    def configure_args(self):
        args = super().configure_args()

        if '+ham' in self.spec:
            args.append('--enable-atm-phy-echam-submodels')
            args.append('--enable-hammoz')

        return args
