{
	'repo_type' : 'git',
	'url' : 'https://github.com/google/highway.git',
	# 'depth_git': 0,
	'conf_system' : 'cmake',
	'build_system' : 'ninja',
	'source_subfolder' : 'build',
	'env_exports' : { # 2020.06.19
		'CFLAGS'   : ' -Wa,-muse-unaligned-vector-move {original_cflags}',
		'CXXFLAGS' : ' -Wa,-muse-unaligned-vector-move {original_cflags}',
		'CPPFLAGS' : ' -Wa,-muse-unaligned-vector-move {original_cflags}',
	},
	'configure_options' : 
		'.. {cmake_prefix_options} '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} '
        '-DBUILD_SHARED_LIBS=false '
        '-DCMAKE_BUILD_TYPE=Release '
        '-DBUILD_TESTING=OFF '
        '-DHWY_CMAKE_ARM7=OFF '
        '-DCMAKE_GNUtoMS=OFF '
        '-DHWY_ENABLE_EXAMPLES=OFF '
        '-DHWY_ENABLE_CONTRIB=OFF '
        '-DHWY_ENABLE_INSTALL=ON '
        '-DHWY_WARNINGS_ARE_ERRORS=OFF '
	,
	'update_check' : { 'type' : 'git', },
	'_info' : { 'version' : None, 'fancy_name' : 'highway' },
}