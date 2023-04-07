{
	'repo_type' : 'git',
	'depth_git': 0,
	# 'branch' : 'v1.3.241',
	'branch':'main', 
	'url' : 'https://github.com/KhronosGroup/Vulkan-Headers.git',
	'recursive_git' : True,
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX={target_prefix}',
	'conf_system' : 'cmake',
	'env_exports' : {
		'CFLAGS'   : ' -DVK_ENABLE_BETA_EXTENSIONS {original_cflags}',
		'CXXFLAGS' : ' -DVK_ENABLE_BETA_EXTENSIONS {original_cflags}',
		'CPPFLAGS' : ' -DVK_ENABLE_BETA_EXTENSIONS {original_cflags}', # 2020.06.20 per https://github.com/fribidi/fribidi/issues/146#issuecomment-646991416
		'LDFLAGS'  : ' -DVK_ENABLE_BETA_EXTENSIONS {original_cflags}',
	},
	'_info' : { 'version' : None, 'fancy_name' : 'Vulkan headers' },
}