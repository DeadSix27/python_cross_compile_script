{
	'repo_type' : 'git',
	'depth_git': 0,
	'url' : 'https://github.com/KhronosGroup/Vulkan-Loader.git',
	# 'branch': 'ad393f9be6c91160e4292ea176c2c8e01efd5d8e',
	'branch': 'master',
	'configure_options' : 
		'.. {cmake_prefix_options} -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX={target_prefix} '
		'-DVULKAN_HEADERS_INSTALL_DIR={target_prefix} '
		'-DBUILD_TESTS=OFF '
		# '-DUPDATE_DEPS=ON '
		'-DUSE_MASM=OFF '
		'-DBUILD_STATIC_LOADER=ON '
        "-DENABLE_WERROR=OFF "
	,
	# 'cpu_count': 1,
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	# 'patches' : [
		# ('vulkan/0001-fix-cross-compiling.patch', '-p1', '..'),
		# ('vulkan/0001-mingw-workarounds.patch','-p1','..'),
	# ],
	# 'env_exports' : { 
	# 	'CFLAGS'   : '-O3 -D_POSIX_C_SOURCE',
	# 	'CXXFLAGS' : '-O3 -D_POSIX_C_SOURCE',
	# 	'CPPFLAGS' : '-O3 -D_POSIX_C_SOURCE',
	# 	'LDFLAGS'  : '-O3 -D_POSIX_C_SOURCE',
	# },
	'regex_replace': {
		'post_install': [
			{
				0: r'(?:[^\r\n]+)?libdir=(?:[^\r\n]+)?',
				'in_file': '{pkg_config_path}/vulkan.pc',
				# 'out_file': '{pkg_config_path}/vulkan.pc'
			},
			{
				0: r'exec_prefix=([^\r\n]+)',
				1: r'exec_prefix=\1\nlibdir=${{exec_prefix}}/lib\n',
				'in_file': '{pkg_config_path}/vulkan.pc',
				# 'out_file': '{pkg_config_path}/vulkan.pc'
			},
			{
				0: r'-lvulkan-1.dll$',
				1: r'-l:libvulkan-1.dll.a',
				'in_file': '{pkg_config_path}/vulkan.pc',
				# 'out_file': '{pkg_config_path}/vulkan.pc'
			},
		]
	},
	'depends_on' : [ 'vulkan_headers' ], # 'vulkan-d3dheaders',
	'_info' : { 'version' : None, 'fancy_name' : 'Vulkan Loader' },
}