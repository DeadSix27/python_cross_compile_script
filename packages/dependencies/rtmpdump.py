{
	'repo_type' : 'git',
	'url' : 'https://git.ffmpeg.org/rtmpdump.git',
	'needs_configure' : False,
	'install_options' : 'SYS=mingw CRYPTO=GNUTLS LIB_GNUTLS="-L{target_prefix}/lib -lpthread -lgnutls -lhogweed -lnettle -lgmp -lcrypt32 -lws2_32 -lintl -liconv -lz -lpthread " OPT=-O3 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={target_prefix}',
	'build_options' : 'SYS=mingw CRYPTO=GNUTLS LIB_GNUTLS="-L{target_prefix}/lib -lpthread -lgnutls -lhogweed -lnettle -lgmp -lcrypt32 -lws2_32 -lintl -liconv -lz  -lpthread " OPT=-O3 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={target_prefix}',
	#'run_post_install' :(
	#	'sed -i.bak \'s/-lrtmp -lz/-lrtmp -lwinmm -lz/\' "{pkg_config_path}/librtmp.pc"',
	#),
	'depends_on' : [
		'gnutls',
		'zlib',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'rtmpdump' },
}