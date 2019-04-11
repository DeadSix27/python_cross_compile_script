{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://download.gnome.org/sources/glib/2.58/glib-2.58.3.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '8f43c31767e88a25da72b52a40f3301fefc49a665b56dc10ee7cc9565cbe7481' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/glib-2.58.3.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '8f43c31767e88a25da72b52a40f3301fefc49a665b56dc10ee7cc9565cbe7481' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --with-pcre=internal --with-threads=posix --disable-fam --disable-shared --disable-libmount',
	'depends_on' : [ 'libffi','gettext', 'libelf' ],
	'run_post_patch' : [
		'if [ ! -f "INSTALL" ] ; then touch INSTALL ; fi',
		'echo \'<<EOF\nEXTRA_DIST =\nCLEANFILES =\nEOF\' > gtk-doc.make',
		'sed -i.bak "s/SUBDIRS = . m4macros glib gmodule gthread gobject gio po docs tests subprojects/SUBDIRS = . m4macros glib gmodule gthread gobject gio po subprojects/" Makefile.am',
		'autoreconf -fiv',
	],
	'patches' : [
		( 'glib2/0001-Use-CreateFile-on-Win32-to-make-sure-g_unlink-always.patch', '-p1' ),
		( 'glib2/0001-win32-Make-the-static-build-work-with-MinGW-when-pos.patch', '-p1' ),
		( 'glib2/0001-disable-some-tests-when-static.patch', '-p1' ),
		( 'glib2/0001-Revert-tests-W32-ugly-fix-for-sscanf-format.patch', '-p1' ),
	],
	'update_check' : { 'url' : 'https://developer.gnome.org/glib/', 'type' : 'httpregex', 'regex' : r'<a class="doc-link" href="2.58/" lang="">(?P<version_num>[\d.]+)<\/a>' },
	'_info' : { 'version' : '2.58.3', 'fancy_name' : 'glib2' },
}
# ########## As reference when we have to switch to cmake, which still fails to build so..
#{
#	'repo_type' : 'archive',
#	# 'download_locations' : [
#		# { 'url' : 'https://download.gnome.org/sources/glib/2.58/glib-2.58.2.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'c7b24ed6536f1a10fc9bce7994e55c427b727602e78342821f1f07fb48753d4b' }, ], },
#		# { 'url' : 'https://fossies.org/linux/misc/glib-2.58.2.tar.xz/', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'c7b24ed6536f1a10fc9bce7994e55c427b727602e78342821f1f07fb48753d4b' }, ], },
#	# ],
#	'url' : 'https://download.gnome.org/sources/glib/2.58/glib-2.58.3.tar.xz',
#	# 'run_post_patch' : [
#		# 'if [ ! -f "INSTALL" ] ; then touch INSTALL ; fi',
#		# 'echo \'<<EOF\nEXTRA_DIST =\nCLEANFILES =\nEOF\' > gtk-doc.make',
#		# 'sed -i.bak "s/SUBDIRS = . m4macros glib gmodule gthread gobject gio po docs tests subprojects/SUBDIRS = . m4macros glib gmodule gthread gobject gio po subprojects/" Makefile.am',
#		# 'autoreconf -fiv',
#	# ],
#	'conf_system' : 'meson',
#	'build_system' : 'ninja',
#	'source_subfolder' : 'build',
#	'configure_options' : 
#		'--prefix={target_prefix} '
#		'--libdir={target_prefix}/lib '
#		'--default-library=static '
#		'--buildtype=plain '
#		'--backend=ninja '
#		# '-Dbuild_tests=false '
#		# '-Dbuild_tools=false '
#		'--buildtype=release '
#		'-Dinstalled_tests=false '
#		'-Dinternal_pcre=true '
#		'-Diconv=native '#          [libc, gnu, native]
#		'-Dforce_posix_threads=true '
#		'--cross-file={meson_env_file} ./ ..'
#		# --with-pcre=internal --with-threads=posix --disable-fam --disable-shared --disable-libmount
#	,
#	'env_exports' : {
#		'LDFLAGS' : '-liconv',
#	},
#	'patches' : [
#		( 'glib2/0001-Use-CreateFile-on-Win32-to-make-sure-g_unlink-always.patch', '-p1', '..' ),
#		( 'glib2/0001-win32-Make-the-static-build-work-with-MinGW-when-pos.patch', '-p1', '..' ),
#		( 'glib2/0001-disable-some-tests-when-static.patch', '-p1', '..' ),
#		( 'glib2/0001-Revert-tests-W32-ugly-fix-for-sscanf-format.patch', '-p1', '..' ),
#		
#	],
#	'depends_on' : [ 'libffi', 'gettext' ],
#	'update_check' : { 'url' : 'https://developer.gnome.org/glib/', 'type' : 'httpregex', 'regex' : r'<a class="doc-link" href="2.58/" lang="">(?P<version_num>[\d.]+)<\/a>' },
#	'_info' : { 'version' : '2.58.2', 'fancy_name' : 'glib2' },
#}