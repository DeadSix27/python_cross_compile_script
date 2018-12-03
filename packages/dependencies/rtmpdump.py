{
	'repo_type' : 'git',
	'url' : 'https://git.ffmpeg.org/rtmpdump.git',
	'needs_configure' : False,
	# doesn't compile with openssl1.1
	'install_options' : 'SYS=mingw CRYPTO=GNUTLS LIB_GNUTLS="-L{target_prefix}/lib -lgnutls -lhogweed -lnettle -lgmp -lcrypt32 -lz" OPT=-O2 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={target_prefix}',
	'build_options' : 'SYS=mingw CRYPTO=GNUTLS LIB_GNUTLS="-L{target_prefix}/lib -lgnutls -lhogweed -lnettle -lgmp -lcrypt32 -lz"	 OPT=-O2 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={target_prefix}',
	# 'install_options' : 'SYS=mingw CRYPTO=GNUTLS OPT=-O2 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={target_prefix} LIB_GNUTLS="-L{target_prefix}/lib -lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -liconv -lz -lintl -liconv"',
	# 'build_options' : 'SYS=mingw CRYPTO=GNUTLS OPT=-O2 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={target_prefix} LIB_GNUTLS="-L{target_prefix}/lib -lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -liconv -lz -lintl -liconv"',
	'run_post_install' :(
		'sed -i.bak \'s/-lrtmp -lz/-lrtmp -lwinmm -lz/\' "{pkg_config_path}/librtmp.pc"',
	),
	'depends_on' : [
		'gnutls',
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'rtmpdump' },
}