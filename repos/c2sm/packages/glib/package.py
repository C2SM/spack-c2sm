from spack import *


class Glib(Package):
    """GLib is a general-purpose utility library, which provides many useful
       data types, macros, type conversions, string utilities, file utilities,
       a mainloop abstraction, and so on."""

    homepage = "https://developer.gnome.org/glib/"
    url = "https://ftp.gnome.org/pub/gnome/sources/glib/2.27/glib-2.27.0.tar.gz"

    version('2.27.0',
            sha256=
            'ab6ba044e1533c5857f0a21f32a4f37299819c9d8a61447f2bc3416f5fb81ce3')

    depends_on('pkgconfig', type='build')
    depends_on('gettext', type='build')
    depends_on('libiconv', type='build')

    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix))
        make()
        make('install')
