{
	'repo_type' : 'git',
	'url' : 'https://github.com/uclouvain/openjpeg.git',
	'conf_system' : 'cmake',
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS:bool=off',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'openjpeg' },
}