{
	'repo_type' : 'archive',
	'url' : 'https://developer.gnome.org/glib/glib-html-2.54.3.tar.gz',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --with-pcre=system --with-threads=win32 --disable-fam --disable-shared',
	'depends_on' : [ 'pcre2' ],
	'patches' : [
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/0001-Use-CreateFile-on-Win32-to-make-sure-g_unlink-always.patch','-Np1'),
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/0004-glib-prefer-constructors-over-DllMain.patch'               ,'-Np1'),
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/0017-GSocket-Fix-race-conditions-on-Win32-if-multiple-thr.patch','-p1' ),
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/0027-no_sys_if_nametoindex.patch'                               ,'-Np1'),
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/0028-inode_directory.patch'                                     ,'-Np1'),
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/revert-warn-glib-compile-schemas.patch'                         ,'-Rp1'),
		# ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/use-pkgconfig-file-for-intl.patch'                              ,'-p0' ),

	],
	'run_post_patch' : [
		'./autogen.sh NOCONFIGURE=1',
	],
	'_info' : { 'version' : '2.54.3', 'fancy_name' : 'glib2' },
}