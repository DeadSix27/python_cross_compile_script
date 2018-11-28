{
	'repo_type' : 'git',
	'url' : 'https://github.com/libjpeg-turbo/libjpeg-turbo.git',
	'conf_system' : 'cmake',
	'configure_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DENABLE_STATIC=ON -DENABLE_SHARED=OFF -DCMAKE_BUILD_TYPE=Release',
	'patches': [
		['https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libjpeg-turbo/0001-libjpeg-turbo-git-mingw-compat.patch', '-p1'],
		['https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libjpeg-turbo/0002-libjpeg-turbo-git-libmng-compat.patch', '-p1'],
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libjpeg-turbo' },
}