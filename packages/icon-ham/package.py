from spack import *
from spack.pkg.mch.icon import Icon


class IconHam(Icon):

    @run_before('configure')
    def generate_hammoz_nml(self):
        if '+ham' in self.spec:
            with working_dir('./externals/atm_phy_echam_submodels/namelists'):
                make()

    def configure_args(self):
        args = Icon.configure_args()

        if '+ham' in self.spec:
            args.append('--enable-atm-phy-echam-submodels')
            args.append('--enable-hammoz')

        return args
