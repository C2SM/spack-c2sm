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


class IconDsl(Icon):
    git = 'git@github.com:C2SM/icon-exclaim.git'

    maintainers('jonasjucker', 'huppd')

    version('develop', submodules=True)
    version('icon-dsl', branch='use_icon4py_from_uenv', submodules=True)

    # EXCLAIM-GT4Py specific features:
    dsl_values = ('substitute', 'verify', 'serialize', 'nvtx')
    variant('dsl',
            default='none',
            validator=validate_variant_dsl,
            values=('none', ) + dsl_values,
            description='Build with GT4Py dynamical core',
            multi=True)

    for x in dsl_values:
        # depends_on('py-icon4py', when='dsl={0}'.format(x))
        depends_on('icon4py', type="build", when=f"dsl={x}")
        # depends_on('py-gridtools-cpp', when='dsl={0}'.format(x))
        # depends_on('boost', when='dsl={0}'.format(x))
        conflicts('^python@:3.9,3.11:', when='dsl={0}'.format(x))

    def setup_build_environment(self, env):
        super().setup_build_environment(env)

        # # path to the generated py2fgen wrappers
        # build_py2f = os.path.join(self.stage.source_path, "src", "build_py2f")

        # env.set("PY2F_CPU_LDFLAGS", f"-L{build_py2f}")
        # env.set("PY2F_CPU_CFLAGS", f"-I{build_py2f}")
        # env.set("PY2F_GPU_LDFLAGS", f"-L{build_py2f}")
        # env.set("PY2F_GPU_CFLAGS", f"-I{build_py2f}")

        # env.set("PY2F_LIBS", "-licon4py_bindings")

    def configure_args(self):
        args = super().configure_args()
        print()
        print("super args: ", args)
        print()
        super_libs = args.pop()
        print()
        print('super libs', super_libs)
        print()
        super_ldflags = args.pop()
        print()
        print('super ldflags', super_ldflags)
        print()
        print(args)

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

            # path to the generated py2fgen wrappers
            # build_py2f = os.path.join(self.stage.source_path, "src", "build_py2f")

            # # Copy bindings into the ICON source tree so autotools can see them
            # icon4py_prefix = self.spec["icon4py"].prefix
            # #     print(f"icon4py_prefix: {icon4py_prefix}")
            # bindings_dir = os.path.join(icon4py_prefix, "src")
            # print(f"bindings_dir: {bindings_dir}")

        #     print(f"dst_dir: {build_py2f}")
        #     os.makedirs(build_py2f, exist_ok=True)

        #     if os.path.isdir(bindings_dir):
        #         # copy into a subdir of the current build dir
        #         for f in os.listdir(bindings_dir):
        #             src_file = os.path.join(bindings_dir, f)
        #             dst_file = os.path.join(build_py2f, f)
        #             if os.path.isfile(src_file):
        #                 shutil.copy2(src_file, dst_file)
        #             print(f"dst_file: {os.path.realpath(dst_file)}")

        if dsl != ('none', ):
            icon4py_prefix = self.spec["icon4py"].prefix
            bindings_dir = os.path.join(icon4py_prefix, "src")
            args.append(f"{super_ldflags} -L{bindings_dir}")
            args.append(f"{super_libs} {libs.link_flags} -licon4py_bindings")
        else:
            args.append(f"{super_ldflags}")
            args.append(f"{super_libs} {libs.link_flags}")
        print()
        print('ICON DSL args:', args)
        print()
        return args
