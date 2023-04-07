{
	'repo_type' : 'git',
	'url' : 'https://github.com/Haivision/srt.git',
	'source_subfolder' : '_build',
	'conf_system' : 'cmake',
	'depends_on' : [ 'gettext', 'libressl' ],
	'configure_options' :
		'.. {cmake_prefix_options} '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} '
		'-DENABLE_STATIC=1 -DUSE_STATIC_LIBSTDCXX=1 '
		# '-DUSE_ENCLIB=gnutls '
		'-DUSE_ENCLIB=openssl '
		'-DOPENSSL_USE_STATIC_LIBS=ON '
		'-DUSE_OPENSSL_PC=OFF '
		'-DENABLE_SHARED=0 '
		'-DENABLE_APPS=OFF'
	,
	'_info' : { 'version' : None, 'fancy_name' : 'libmysofa' },
}