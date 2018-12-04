{
	'repo_type' : 'git',
	'url' : 'https://github.com/hoene/libmysofa',
	#'branch' : '16d77ad6b4249c3ba3b812d26c4cbb356300f908',
	'source_subfolder' : '_build',
	'conf_system' : 'cmake',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS:bool=off -DBUILD_TESTS=no',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libmysofa' },
}