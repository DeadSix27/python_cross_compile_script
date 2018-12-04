{
	'repo_type' : 'archive',
	'url' : 'https://download.gnome.org/sources/glib/2.58/glib-2.58.1.tar.xz',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --with-pcre=internal --with-threads=posix --disable-fam --disable-shared --disable-libmount',
	'depends_on' : [ 'libffi','gettext' ],
	'run_post_patch' : [
		'if [ ! -f "INSTALL" ] ; then touch INSTALL ; fi',
		'autoreconf -fiv',
	],
	'_info' : { 'version' : '2.58.1', 'fancy_name' : 'glib2' },
}