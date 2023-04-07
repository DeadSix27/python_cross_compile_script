{
	'repo_type' : 'git',
	'rename_folder' : 'glslang',
	'url' : 'https://github.com/KhronosGroup/glslang.git',
	'depth_git': 0,
	# 'branch': '12.0.0',
	'branch': 'main',
	'patches' : [
		( 'https://github.com/KhronosGroup/glslang/pull/3144.patch', '-p1', '..' ), # Include <cstdint> header in Common.h #3144 
	],
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DCMAKE_BUILD_TYPE=Release',
	'_info' : { 'version' : None, 'fancy_name' : 'glslang' },
}