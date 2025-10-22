from spack.pkg.c2sm.icon import Icon
import shutil
import os
import re
from collections import defaultdict
import spack.error as error


def validate_variant_dsl(pkg, name, value):
    set_mutual_excl = set(['substitute', 'verify', 'serialize'])
    set_input_var = set(value)
    if len(set_mutual_excl.intersection(set_input_var)) > 1:
        raise error.SpecError(
            'Cannot have more than one of (substitute, verify, serialize) in the same build'
        )


class IconExclaim(Icon):
    git = 'git@github.com:C2SM/icon-exclaim.git'

    maintainers('jonasjucker', 'huppd')

    version('develop', branch='icon-dsl', submodules=True)

    # EXCLAIM-GT4Py specific features:
    dsl_values = ('substitute', 'verify', 'serialize', 'nvtx')
    variant('dsl',
            default='none',
            validator=validate_variant_dsl,
            values=('none', ) + dsl_values,
            description='Build with GT4Py dynamical core',
            multi=True)

    for x in dsl_values:
        depends_on('icon4py', type="build", when=f"dsl={x}")
        conflicts('^python@:3.9,3.11:', when='dsl={0}'.format(x))

    def configure_args(self):
        args = super().configure_args()

        super_libs = args.pop()
        super_ldflags = args.pop()

        libs = LibraryList([])
        flags = defaultdict(list)

        # Check for DSL variants and set corresponding options
        dsl = self.spec.variants['dsl'].value
        if dsl != ('none', ):
            if 'substitute' in dsl:
                args.append('--enable-py2f=substitute')
            elif 'verify' in dsl:
                args.append('--enable-py2f=verify')
            elif 'serialize' in dsl:
                raise error.UnsupportedPlatformError(
                    'serialize mode is not supported yet by icon-liskov')

            icon4py_prefix = self.spec["icon4py"].prefix
            bindings_dir = os.path.join(icon4py_prefix, "src")
            args.append(
                f"{super_ldflags} -L{bindings_dir} -Wl,-rpath,{bindings_dir}")
            args.append(f"{super_libs} {libs.link_flags} -licon4py_bindings")

        else:
            args.append(f"{super_ldflags}")
            args.append(f"{super_libs} {libs.link_flags}")

        return args

    def build(self, spec, prefix):
        # Check the variant
        dsl = self.spec.variants['dsl'].value
        if dsl != ('none', ):
            file = "icon4py_bindings.f90"

            bindings_dir = os.path.join(self.spec["icon4py"].prefix, "src")
            src_file = os.path.join(bindings_dir, file)

            build_py2f_dir = os.path.join(self.stage.source_path, "src",
                                          "build_py2f")
            os.makedirs(build_py2f_dir, exist_ok=True)
            dest_file = os.path.join(build_py2f_dir, file)

            # Copy only if the file is missing
            if not os.path.exists(dest_file) or os.path.getmtime(
                    src_file) > os.path.getmtime(dest_file):
                shutil.copy(src_file, dest_file)
                print(
                    f"Copied {src_file} to build directory {dest_file} because +dsl is enabled"
                )

        # Proceed with the normal build
        super().build(spec, prefix)
