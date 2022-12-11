{
    # "_already_built": True,
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/flac.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DBUILD_PROGRAMS=OFF -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF -DINSTALL_MANPAGES=OFF -DVERSION=1.3.3 -DCMAKE_BUILD_TYPE=Release',
	'patches': [
		# ('flac/0001-mingw-fix.patch', '-p1', '..'),
		#('flac/01.patch', '-p1', '..'),
	],
	# 'env_exports' : {
	# 	'LIBS' : '-lssp',
	# },
	#'custom_cflag' : '-O3',
	'regex_replace': {
		'post_patch': [
			{
				0: r'add_subdirectory\("microbench"\)',
				'in_file': '../CMakeLists.txt'
			},
			# {
			# 	0: r'add_definitions\(-DHAVE_CONFIG_H\)',
			# 	1: r'add_definitions\(-DHAVE_CONFIG_H -D_FORTIFY_SOURCE=0\)',
			# 	'in_file': '../src/CMakeLists.txt'
			# },
		],
	},
	'depends_on' : [
		'libogg',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'flac (library)' },
}