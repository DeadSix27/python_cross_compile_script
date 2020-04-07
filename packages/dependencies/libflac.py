{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/flac.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DBUILD_PROGRAMS=OFF -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF -DVERSION=1.3.3 -DCMAKE_BUILD_TYPE=Release',
	'patches': [
		('flac/0001-mingw-fix.patch', '-p1', '..'),
	],
	'regex_replace': {
		'post_patch': [
			{
				0: r'add_subdirectory\("microbench"\)',
				'in_file': '../CMakeLists.txt'
			},
		],
	},
	'depends_on' : [
		'libogg',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'flac (library)' },
}