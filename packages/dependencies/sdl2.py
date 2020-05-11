{
	# 'repo_type' : 'mercurial',
	# 'url' : 'https://hg.libsdl.org/SDL',
	# 'folder_name' : 'sdl2_hg',
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://www.libsdl.org/release/SDL2-2.0.12.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '349268f695c02efbc9b9148a70b85e58cefbbf704abd3e91be654db7f1e2c863' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/SDL2-2.0.12.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '349268f695c02efbc9b9148a70b85e58cefbbf704abd3e91be654db7f1e2c863' }, ], },
	],
	'conf_system' : 'cmake',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DSDL_SHARED=OFF',
	'source_subfolder': '_build',

	'regex_replace': {
		'post_patch': [
			{
				0: r'if\(NOT WINDOWS OR CYGWIN\)',
				1: r'if(NOT MSVC OR CYGWIN)',
				'in_file': '../CMakeLists.txt' # why "WINDOWS", why not "MSVC"...
			},
			{
				0: r'if\(NOT \(WINDOWS OR CYGWIN\)\)',
				1: r'if(NOT (MSVC OR CYGWIN))',
				'in_file': '../CMakeLists.txt'
			},
		],
	},
	'_info' : { 'version' : None, 'fancy_name' : 'SDL2' },
}