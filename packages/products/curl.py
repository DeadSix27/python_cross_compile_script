#type:ignore
{
    'do_not_git_update':True,
	'repo_type' : 'git',
	# 'debug_confighelp_and_exit' : True,
	'url' : 'https://github.com/curl/curl',
	# 'rename_folder' : 'curl_git',
	# 'env_exports' : {
		# 'LIBS' : '-lcrypt32',
		# 'libsuff' : '/',
	# },
	'patches' : [
		('curl/0001-search-exedir-for-bundle.patch', '-p1', '..' ),
	],

    # 'regex_replace': {
        # 'post_patch': [
            # {
                # 0: r'LIBS="-lgnutls  $LIBS"',
                # 1: r'LIBS="-lws2_32 -lgmp -latomic -ladvapi32 -lcrypt32 -lncrypt -lbcrypt -lnettle -lgnutls"',
                # 'in_file': 'configure',
            # },
        # ]
    # },    
	'conf_system' : 'cmake',
	'source_subfolder': '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={output_prefix}/curl_git.installed -DCURL_WINDOWS_SSPI=OFF -DUSE_WINCRYPT=OFF -DCURL_USE_LIBSSH2=OFF -DCURL_USE_OPENSSL=ON -DBUILD_SHARED_LIBS=OFF',

	# 'configure_options' : '--enable-static --with-openssl --disable-shared --target={bit_name2}-{bit_name_win}-gcc --host={target_host} --build=x86_64-linux-gnu --with-libssh2 --with-openssl --with-ca-fallback --without-winssl --prefix={output_prefix}/curl_git.installed --exec-prefix={output_prefix}/curl_git.installed',
	'depends_on' : (
		'zlib', 'libssh2', 'libressl',
	),
	'_info' : { 'version' : None, 'fancy_name' : 'cURL' },
}