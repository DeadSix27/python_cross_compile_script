{
	'repo_type' : 'archive',
	'download_locations' : [
		{ "url" : "https://www.openssl.org/source/openssl-1.1.1-pre8.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "1205cd763dd92c910cc590658a5b0774599e8587d89d6debd948f242b949321e" }, ], },
		{ "url" : "http://ftp.vim.org/pub/ftp/security/openssl/openssl-1.1.1-pre8.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "1205cd763dd92c910cc590658a5b0774599e8587d89d6debd948f242b949321e" }, ], },
	],
	'configure_options' : '{bit_name3} enable-capieng  --prefix={target_prefix} --openssldir={target_prefix}/ssl --cross-compile-prefix={cross_prefix_bare} no-shared no-asm',
	'configure_path' : './Configure',
	'install_target' : 'install_sw', # we don't need the docs..
	'build_options' : 'all',
	'env_exports' : {
		'CROSS_COMPILE' : '{cross_prefix_bare}',
	},
	'run_post_install' : [
		'sed -i.bak 's/Libs: -L${{libdir}} -lcrypto/Libs: -L${{libdir}} -lcrypto -lcrypt32/' "{pkg_config_path}/libcrypto.pc"', # libssh2 doesn't use --static pkgconfig, so we have to do this.
		'sed -i.bak 's/Libs: -L${{libdir}} -lssl/Libs: -L${{libdir}} -lssl -lcrypt32/' "{pkg_config_path}/libssl.pc"', # nor does curl
	],
	'_info' : { 'version' : '1.1.1-pre1', 'fancy_name' : 'openssl' },
}