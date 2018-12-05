{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://sourceforge.net/projects/bs2b/files/libbs2b/3.1.0/libbs2b-3.1.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '6aaafd81aae3898ee40148dd1349aab348db9bfae9767d0e66e0b07ddd4b2528' }, ], },
		{ 'url' : 'http://sourceforge.mirrorservice.org/b/bs/bs2b/libbs2b/3.1.0/libbs2b-3.1.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '6aaafd81aae3898ee40148dd1349aab348db9bfae9767d0e66e0b07ddd4b2528' }, ], },
	],
	'env_exports' : {
		'ac_cv_func_malloc_0_nonnull' : 'yes', # fixes undefined reference to `rpl_malloc'
	},
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'update_check' : { 'url' : 'https://sourceforge.net/projects/bs2b/files/libbs2b/', 'type' : 'sourceforge', },
	'_info' : { 'version' : '3.1.0', 'fancy_name' : 'libbs2b' },
}