from spack.pkg.builtin.libfyaml import Libfyaml as SpackLibfyaml


class Libfyaml(SpackLibfyaml):

    @property
    def libs(self):
        libraries = ['libfyaml']

        libs = find_libraries(libraries,
                              root=self.prefix,
                              shared=True,
                              recursive=True)

        if libs and len(libs) == len(libraries):
            return libs

        msg = 'Unable to recursively locate shared {0} libraries in {1}'
        raise spack.error.NoLibrariesError(
            msg.format(self.spec.name, self.spec.prefix))
