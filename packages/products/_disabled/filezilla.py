{
	'repo_type' : 'svn',
	'folder_name' : 'filezilla_svn',
	'url' : 'https://svn.filezilla-project.org/svn/FileZilla3/trunk',
	'configure_options': '--host={target_host} --prefix={product_prefix}/filezilla_svn.installed --disable-shared --enable-static --disable-manualupdatecheck --disable-autoupdatecheck --with-pugixml=builtin host_os=mingw',
	'run_post_patch' : [
		'autoreconf -fiv',
		'sed -i.bak \'s/extern _SYM_EXPORT gnutls_free/extern gnutls_free/\' "{target_prefix}/include/gnutls/gnutls.h"', #edit gnutls.h and remove the _SYM_EXPORT part apparently...? : https://forum.filezilla-project.org/viewtopic.php?t=1227&start=180
	],
	'depends_on' : [
		'libfilezilla',
		'gnutls',
		'wxwidgets',
		'libsqlite3'
	 ],
	'env_exports' : {
		'LIBGNUTLS_LIBS' : '"-L{target_prefix}/lib -lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -lz"',
		'LIBS' : '-lgnutls',
		'CXXFLAGS' : '-Wall -O2',
	},
	'patches' : [
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/filezilla/0001-remove-32bit-fzshellext.patch','-p1'),
	],
	'run_post_install' : [
		'mv "{target_prefix}/include/gnutls/gnutls.h.bak" "{target_prefix}/include/gnutls/gnutls.h"'
	],
	'packages': {
		'ubuntu' : [ 'wxrc' ],
	},
	'_info' : { 'version' : 'svn (master)', 'fancy_name' : 'FileZilla (64Bit only)' },

}