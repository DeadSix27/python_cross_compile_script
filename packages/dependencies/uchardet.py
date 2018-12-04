{
	'repo_type' : 'git',
	'url' : 'https://anongit.freedesktop.org/git/uchardet/uchardet.git',
	# 'branch' : 'f136d434f0809e064ac195b5bc4e0b50484a474c', #master fails
	'conf_system' : 'cmake',
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DBUILD_BINARY=OFF -DCMAKE_BUILD_TYPE=Release',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'uchardet' },
}