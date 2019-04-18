{
	'repo_type' : 'git',
	'url' : 'https://github.com/KhronosGroup/Vulkan-Loader.git',
	# 'recursive_git' : True, 
	'configure_options' : 
		'.. {cmake_prefix_options} -DVULKAN_HEADERS_INSTALL_DIR={target_prefix} '
		'-DCMAKE_BUILD_TYPE=Release '
		'-DBUILD_TESTS=OFF '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} -DCMAKE_ASM-ATT_COMPILER={mingw_binpath}/{cross_prefix_bare}as '
		'-DBUILD_TESTS=OFF -DENABLE_STATIC_LOADER=ON '
		'-DCMAKE_C_FLAGS=\'-D_WIN32_WINNT=0x0600 -D__STDC_FORMAT_MACROS\' '
		'-DCMAKE_CXX_FLAGS=\'-D__USE_MINGW_ANSI_STDIO -D__STDC_FORMAT_MACROS -fpermissive -D_WIN32_WINNT=0x0600\''
	, #-D_WIN32_WINNT=0x0600 -D__STDC_FORMAT_MACROS" -D__USE_MINGW_ANSI_STDIO -D__STDC_FORMAT_MACROS -fpermissive -D_WIN32_WINNT=0x0600"
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'branch' : 'v1.1.106',
	'patches' : [
		('vulkan/0001-vulkan-loader-cross-compile-static-linking-hacks.patch','-p1','..'),
	],
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lvulkan/Libs: -L${{libdir}} -lvulkan -lshlwapi -lcfgmgr32/\' "{target_prefix}/lib/pkgconfig/vulkan.pc"',
	],
	'depends_on' : [ 'vulkan_headers' ],
	'_info' : { 'version' : None, 'fancy_name' : 'Vulkan Loader' },
}