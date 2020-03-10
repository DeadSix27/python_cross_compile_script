{
	'repo_type' : 'git',
	'url' : 'https://github.com/KhronosGroup/Vulkan-Loader.git',
	# 'branch': '85886d8517aae8e2834825255dc2989adaab62be',
	'configure_options' : 
		'.. {cmake_prefix_options} -DVULKAN_HEADERS_INSTALL_DIR={target_prefix} '
		'-DCMAKE_BUILD_TYPE=Release '
		'-DBUILD_TESTS=OFF '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} '
		'-DBUILD_TESTS=OFF ' #-DENABLE_STATIC_LOADER=ON 
	,
	# 'cpu_count': 1,
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'patches' : [
		# ('vulkan/0001-fix-cross-compiling.patch', '-p1', '..'),
		('vulkan/0001-mingw-workarounds.patch','-p1','..'),
	],
	'regex_replace': {
		'post_install': [
			{
				0: r'(?:[^\r\n]+)?libdir=(?:[^\r\n]+)?',
				'in_file': '{pkg_config_path}/vulkan.pc',
				'out_file': '{pkg_config_path}/vulkan.pc'
			},
			{
				0: r'exec_prefix=([^\r\n]+)',
				1: r'prefix={{target_prefix}}\nexec_prefix=\1\nlibdir=${{exec_prefix}}/lib\n',
				'in_file': '{pkg_config_path}/vulkan.pc',
				'out_file': '{pkg_config_path}/vulkan.pc'
			},
		]
	},
	'depends_on' : [ 'vulkan_headers' ], # 'vulkan-d3dheaders',
	'_info' : { 'version' : None, 'fancy_name' : 'Vulkan Loader' },
}