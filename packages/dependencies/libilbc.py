{
	'repo_type' : 'git',
	'url' : 'https://github.com/dekkers/libilbc.git',
	'branch': 'main',
	'conf_system' : 'cmake',
	'recursive_git': True,
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DCMAKE_BUILD_TYPE=Release',
	'_info' : { 'version' : None, 'fancy_name' : 'libilbc' },
}