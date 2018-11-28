{
	'repo_type' : 'git',
	# 'debug_confighelp_and_exit' : True,
	'url' : 'https://github.com/curl/curl',
	'rename_folder' : 'curl_git',
	'env_exports' : {
		'LIBS' : '-lcrypt32',
		'libsuff' : '/',
	},
	# 'patches' : [
		# ['https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/curl/0001-fix-build-with-libressl.patch', '-p1' ],
	# ],
	'run_post_patch' : [
		'sed -i.bak \'s/SSL_LDFLAGS="-L$LIB_OPENSSL"/SSL_LDFLAGS=""/\' configure.ac',
		'autoreconf -fiv',
	],
	'configure_options': '--enable-static --disable-shared --target={bit_name2}-{bit_name_win}-gcc --host={target_host} --build=x86_64-linux-gnu --with-libssh2 --with-ca-fallback --without-winssl --prefix={product_prefix}/curl_git.installed --exec-prefix={product_prefix}/curl_git.installed',
	'depends_on': (
		'zlib', 'libssh2',
	),
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'cURL' },
}