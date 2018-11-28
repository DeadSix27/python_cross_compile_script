{
	'repo_type' : 'git',
	'url' : 'https://github.com/curl/curl',
	'rename_folder' : 'curl_git',
	'configure_options': '--enable-static --disable-shared --target={bit_name2}-{bit_name_win}-gcc --host={target_host} --build=x86_64-linux-gnu --with-libssh2 --with-gnutls --prefix={target_prefix} --exec-prefix={target_prefix}',
	'patches' : [
		['https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/curl/0001-fix-build-with-libressl.patch', '-p1' ],
	],
	'depends_on': (
		'zlib','libssh2',
	),
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libcurl' },
}