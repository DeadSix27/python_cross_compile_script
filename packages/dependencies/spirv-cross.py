{
	'repo_type' : 'git',
	'rename_folder' : 'spirv-cross',
	'url' : 'https://github.com/KhronosGroup/SPIRV-Cross.git',
	'depth_git': 0,
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : 
		'.. {cmake_prefix_options} '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} '
		'-DSPIRV_CROSS_SHARED=OFF '
		'-DSPIRV_CROSS_STATIC=ON '
		'-DSPIRV_CROSS_ENABLE_TESTS=OFF'
	,
	'run_post_install' : [
		"echo 'prefix={target_prefix}\nexec_prefix=${{prefix}}\nlibdir=${{exec_prefix}}/lib\nincludedir=${{prefix}}/include/spirv_cross\nName: spirv-cross-c-shared\nDescription: C API for SPIRV-Cross\nVersion:\nLibs: -L${{libdir}} -lspirv-cross-c -lspirv-cross-cpp -lspirv-cross-reflect -lspirv-cross-glsl -lspirv-cross-hlsl -lspirv-cross-msl -lspirv-cross-core -lstdc++\nCflags: -I${{includedir}}' > {target_prefix}/lib/pkgconfig/spirv-cross.pc",
	],
	'_info' : { 'version' : None, 'fancy_name' : 'SPIRV Cross' },

}