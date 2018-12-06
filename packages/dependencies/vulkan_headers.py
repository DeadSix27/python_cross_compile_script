{
	'repo_type' : 'git',
	'url' : 'https://github.com/KhronosGroup/Vulkan-Headers.git',
	'recursive_git' : True,
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX={target_prefix}',
	'conf_system' : 'cmake',
	'_info' : { 'version' : None, 'fancy_name' : 'Vulkan headers' },
}