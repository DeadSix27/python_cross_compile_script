{
	'repo_type' : 'archive',
	'url' : 'https://www.openssl.org/source/openssl-1.0.2n.tar.gz',
	'configure_options' : '{bit_name3} --prefix={target_prefix} --cross-compile-prefix={cross_prefix_bare} no-shared no-asm',
	'configure_path' : './Configure',
	'install_target' : 'install_sw', # we don't need the docs..
	'env_exports' : {
		'CROSS_COMPILE' : '{cross_prefix_bare}',
	},
	'_info' : { 'version' : '1.0.2n', 'fancy_name' : 'openssl_1.0' },
}