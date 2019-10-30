{
	'repo_type' : 'git',
	'url' : 'https://github.com/KhronosGroup/Vulkan-Loader.git',
	'configure_options' : 
		'.. {cmake_prefix_options} -DVULKAN_HEADERS_INSTALL_DIR={target_prefix} '
		'-DCMAKE_BUILD_TYPE=Release '
		'-DBUILD_TESTS=OFF '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} -DCMAKE_ASM_COMPILER={mingw_binpath}/{cross_prefix_bare}as '
		'-DBUILD_TESTS=OFF -DENABLE_STATIC_LOADER=ON '
	,
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'patches' : [
		('vulkan/0001-fix-cross-compiling.patch', '-p1', '..'),
	],
	'depends_on' : [ 'vulkan_headers' ], # 'vulkan-d3dheaders',
	'_info' : { 'version' : None, 'fancy_name' : 'Vulkan Loader' },
}