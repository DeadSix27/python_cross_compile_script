{
	'repo_type' : 'git',
	'url' : 'https://github.com/Haivision/srt.git',
	'source_subfolder' : '_build',
	'conf_system' : 'cmake',
	'depends_on' : [ 'gettext', 'gnutls' ],
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DENABLE_STATIC=1 -DUSE_STATIC_LIBSTDCXX=1 -DUSE_ENCLIB=gnutls -DENABLE_SHARED=0 -DENABLE_APPS=OFF',
	'_info' : { 'version' : None, 'fancy_name' : 'libmysofa' },
}