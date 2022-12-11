{
	'repo_type' : 'git',
	'url' : 'https://github.com/libsdl-org/SDL',
	'depth_git': 0,
	'branch': 'SDL2',
	'env_exports' : {
		'DXSDK_DIR'  : '{target_prefix}/include',
	},

	# 'do_not_git_update': True,
	'conf_system' : 'cmake',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DSDL_SHARED=OFF',
	'source_subfolder': '_build',
	'regex_replace': {
		'post_patch': [
			# {
			# 	0: r'if\(NOT WINDOWS OR CYGWIN\)',
			# 	1: r'if(NOT MSVC OR CYGWIN)',
			# 	'in_file': '../CMakeLists.txt' # why "WINDOWS", why not "MSVC"...
			# },
			# {
			# 	0: r'if\(NOT \(WINDOWS OR CYGWIN\)\)',
			# 	1: r'if(NOT (MSVC OR CYGWIN))',
			# 	'in_file': '../CMakeLists.txt'
			# },
			{
				0: r'if\(NOT WINDOWS OR CYGWIN OR MINGW\)',
				1: r'if(NOT APPLE)',
				'in_file': '../CMakeLists.txt'
			},
			{
				0: r'if\(NOT \(WINDOWS OR CYGWIN OR MINGW\)\)',
				1: r'if(NOT APPLE)',
				'in_file': '../CMakeLists.txt'
			},
			
		],
	},
	'_info' : { 'version' : None, 'fancy_name' : 'SDL2' },
}