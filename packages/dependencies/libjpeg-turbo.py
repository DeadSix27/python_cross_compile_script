{
	'repo_type' : 'git',
	'url' : 'https://github.com/libjpeg-turbo/libjpeg-turbo.git',
	'branch': 'main',
	'conf_system' : 'cmake',
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DENABLE_STATIC=ON -DENABLE_SHARED=OFF -DCMAKE_BUILD_TYPE=Release',
	'patches' : [
		('libjpeg-turbo/0001-libjpeg-turbo-git-mingw-compat.patch', '-p1'),
		('libjpeg-turbo/0002-libjpeg-turbo-git-libmng-compat.patch', '-p1'),
	],
	'_info' : { 'version' : None, 'fancy_name' : 'libjpeg-turbo' },
}