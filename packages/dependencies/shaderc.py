{
	'repo_type' : 'git',
	'url' : 'https://github.com/google/shaderc.git',
	# 'depth_git': False,
	# 'branch': '3f24b6829b3e7da9c97b779402311ece81264ca8', # libshaderc_spvc/src/spvc.cc:71:33: error: returning reference to temporary [-Werror=return-local-addr]
	'configure_options' :
		'cmake .. {cmake_prefix_options} '
		'-DCMAKE_BUILD_TYPE=Release '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} '
		'-DSHADERC_SKIP_INSTALL=ON '
		'-DSHADERC_SKIP_TESTS=ON '
		'-DSHADERC_ENABLE_SPVC=ON '
	,
	'source_subfolder' : '_build',
	'conf_system' : 'cmake',
	'needs_make_install' : False,
	'build_options' : '',
	'run_post_patch' : [
		'!SWITCHDIR|../third_party',
		'ln -snf {inTreePrefix}/glslang/ glslang',
		'ln -snf {inTreePrefix}/spirv-headers/ spirv-headers',
		'ln -snf {inTreePrefix}/spirv-tools/ spirv-tools',
		'ln -snf {inTreePrefix}/spirv-cross spirv-cross',
		'!SWITCHDIR|../_build',
		"sed -i 's/add_subdirectory(examples)/#add_subdirectory(examples)/g' ../CMakeLists.txt",
	],
	'run_post_build' : [
		'cp -rv "../libshaderc/include/shaderc" "{target_prefix}/include/"',
		'cp -rv "../libshaderc_util/include/libshaderc_util" "{target_prefix}/include/"',
		'cp -rv "libshaderc/libshaderc_combined.a" "{target_prefix}/lib/libshaderc_combined.a"',
	],
	'depends_on' : ['glslang', 'spirv-headers', 'spirv-tools', 'spirv-cross', ],
	'_info' : { 'version' : None, 'fancy_name' : 'shaderc' },
}