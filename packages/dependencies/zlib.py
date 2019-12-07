{
	'repo_type' : 'git',
	'url' : 'https://github.com/madler/zlib.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DAMD64=ON -DCMAKE_BUILD_TYPE=Release',
	'patches' : [
		('zlib/0001-remove-tests-examples.patch', '-p1', '..'),
	],
	'_info' : { 'version' : None, 'fancy_name' : 'zlib' },
}