{
	'repo_type' : 'git',
	'rename_folder' : 'glslang',
	'url' : 'https://github.com/KhronosGroup/glslang.git',
	'depth_git': 0,

	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DCMAKE_BUILD_TYPE=Release',

	# 'branch': '3ed344dd784ecbbc5855e613786f3a1238823e56', 
	#'needs_make' : False,
	#'needs_make_install' : False,
	#'needs_configure' : False,
	'recursive_git' : True,
	'_info' : { 'version' : None, 'fancy_name' : 'glslang' },
}