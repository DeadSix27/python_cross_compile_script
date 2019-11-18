{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/flac',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DENABLE_STATIC_RUNTIME=ON -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF -DVERSION=1.3.3 -DCMAKE_BUILD_TYPE=Release',
	'custom_cflag' : '-O3 -D_FORTIFY_SOURCE=0',
	'patches': [
		('flac/0001-mingw-fix.patch', '-p1', '..'),
	],
	'depends_on' : [
		'libogg',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'flac (library)' },
}