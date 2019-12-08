{
	'repo_type' : 'git',
	'url' : 'https://github.com/json-c/json-c.git',
	'conf_system' : 'cmake',
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_TESTING=OFF -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release -DENABLE_RDRAND=ON -DENABLE_THREADING=ON',
	'_info' : { 'version' : None, 'fancy_name' : 'json-c' },
}