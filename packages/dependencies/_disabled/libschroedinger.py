{
	'repo_type' : 'archive',
	'url' : 'https://download.videolan.org/contrib/schroedinger/schroedinger-1.0.11.tar.gz',
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'run_post_configure': (
		'sed -i.bak 's/testsuite//' Makefile',
	),
	'run_post_install': (
		'sed -i.bak 's/-lschroedinger-1.0$/-lschroedinger-1.0 -lorc-0.4/' "{pkg_config_path}/schroedinger-1.0.pc"',
	),
	'depends_on' : [ 'orc' ],
	'_info' : { 'version' : '1.0.11', 'fancy_name' : 'schroedinger' },

}