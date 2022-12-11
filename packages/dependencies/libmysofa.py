{
	'repo_type' : 'git',
	'url' : 'https://github.com/hoene/libmysofa',
	'branch' : 'main',
	'source_subfolder' : '_build',
	'conf_system' : 'cmake',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS:bool=off -DBUILD_TESTS=no',
	'_info' : { 'version' : None, 'fancy_name' : 'libmysofa' },
}