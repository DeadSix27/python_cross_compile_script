{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://download.gnome.org/sources/glib/2.58/glib-2.58.2.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'c7b24ed6536f1a10fc9bce7994e55c427b727602e78342821f1f07fb48753d4b' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/glib-2.58.2.tar.xz/', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'c7b24ed6536f1a10fc9bce7994e55c427b727602e78342821f1f07fb48753d4b' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --with-pcre=internal --with-threads=posix --disable-fam --disable-shared --disable-libmount',
	'depends_on' : [ 'libffi','gettext' ],
	'run_post_patch' : [
		'if [ ! -f "INSTALL" ] ; then touch INSTALL ; fi',
		'echo \'<<EOF\\nEXTRA_DIST =\\nCLEANFILES =\\nEOF\' > gtk-doc.make',
		'sed -i.bak "s/SUBDIRS = . m4macros glib gmodule gthread gobject gio po docs tests subprojects/SUBDIRS = . m4macros glib gmodule gthread gobject gio po subprojects/" Makefile.am',
		'autoreconf -fiv',
	],
	'patches' : [
		( 'glib2/0001-win32-Make-the-static-build-work-with-MinGW-when-pos.patch', '-p1' ),
	],
	'update_check' : { 'url' : 'https://developer.gnome.org/glib/', 'type' : 'httpregex', 'regex' : r'<a class="doc-link" href="2.58/" lang="">(?P<version_num>[\d.]+)<\/a>' },
	'_info' : { 'version' : '2.58.2', 'fancy_name' : 'glib2' },
}