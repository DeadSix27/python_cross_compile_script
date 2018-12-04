{
	'repo_type' : 'git',
	'url' : 'https://github.com/dlfcn-win32/dlfcn-win32.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DBUILD_TESTS=0',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'dlfcn win32' },
}