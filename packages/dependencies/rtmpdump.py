{
	'repo_type' : 'git',
	'url' : 'https://git.ffmpeg.org/rtmpdump.git',
	'needs_configure' : False,
	'patches': [
		( 'rtmpdump/0001-Add-support-for-LibreSSL.patch', '-p1' )
	],
	# 'install_options' : 'SYS=mingw CRYPTO=GNUTLS LIB_GNUTLS="!CMD(pkg-config --libs --static gnutls)CMD!" OPT=-O3 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={target_prefix}',
	# 'build_options' : 'SYS=mingw CRYPTO=GNUTLS LIB_GNUTLS="!CMD(pkg-config --libs --static gnutls)CMD!" OPT=-O3 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={target_prefix}',	

	'install_options' : 'SYS=mingw CRYPTO=OPENSSL LIB_OPENSSL="!CMD(pkg-config --libs --static libssl)CMD! -lz" OPT=-O3 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={target_prefix}',
	'build_options' : 'SYS=mingw CRYPTO=OPENSSL LIB_OPENSSL="!CMD(pkg-config --libs --static libssl)CMD! -lz" OPT=-O3 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={target_prefix}',
	
	#'run_post_install' :(
	#	'sed -i.bak \'s/-lrtmp -lz/-lrtmp -lwinmm -lz/\' "{pkg_config_path}/librtmp.pc"',
	#),
	#'custom_cflag' : '-O3',
	'depends_on' : [
		'libressl',
		'zlib',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'rtmpdump' },
}