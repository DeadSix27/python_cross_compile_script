{
	'repo_type' : 'mercurial',
	'url' : 'https://hg.libsdl.org/SDL',
	'folder_name' : 'sdl2_hg',

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