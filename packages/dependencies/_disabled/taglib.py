{
	'repo_type' : 'archive',
	'url' : 'http://taglib.org/releases/taglib-1.11.1.tar.gz',
	'conf_system' : 'cmake',
	'configure_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DENABLE_STATIC_RUNTIME=ON -DWITH_MP4=ON -DWITH_ASF=ON',
}