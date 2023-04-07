# type: ignore
{
	'repo_type' : 'git',
	'url' : 'https://github.com/google/shaderc.git',
	'depth_git': 0,
	# 'branch': 'v2023.1',
	'branch':'main', 
	'configure_options' :
		'cmake .. {cmake_prefix_options} '
		'-DCMAKE_BUILD_TYPE=Release '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} '
		'-DSHADERC_SKIP_INSTALL=OFF '
		'-DSHADERC_SKIP_TESTS=ON '
		# '-DSHADERC_ENABLE_TESTS=OFF '
		'-DSHADERC_SKIP_EXAMPLES=ON '
		# '-DSHADERC_ENABLE_EXAMPLES=OFF '
		'-DSHADERC_SKIP_COPYRIGHT_CHECK=ON '
		# '-DSHADERC_ENABLE_COPYRIGHT_CHECK=OFF '
		# '-DSHADERC_ENABLE_SPVC=ON '
	,
	'source_subfolder' : '_build',
	'conf_system' : 'cmake',
	# 'needs_make_install' : False,
	'build_options' : '',
	'run_post_patch' : [
		'!SWITCHDIR|../third_party',
		'ln -snf {inTreePrefix}/glslang/ glslang',
		'ln -snf {inTreePrefix}/spirv-headers/ spirv-headers',
		'ln -snf {inTreePrefix}/spirv-tools/ spirv-tools',
		'ln -snf {inTreePrefix}/spirv-cross spirv-cross',
		'!SWITCHDIR|../_build',
		# "sed -i 's/add_subdirectory(examples)/#add_subdirectory(examples)/g' ../CMakeLists.txt",
		# "sed -i 's/--check/#--check/g' ../CMakeLists.txt",
    	# "sed -i 's/printed_count += 1/#printed_count += 1/g' ../utils/add_copyright.py",
	],

	'regex_replace': {
		'post_install': [
			{
				0: r'lshaderc_shared',
				1: r'lshaderc_combined -lstdc++',
				'in_file': '{pkg_config_path}/shaderc.pc'
			}
		],
	},
	
	# 'run_post_build' : [
	# 	'cp -rv "../libshaderc/include/shaderc" "{target_prefix}/include/"',
	# 	'cp -rv "../libshaderc_util/include/libshaderc_util" "{target_prefix}/include/"',
	# 	'cp -rv "libshaderc/libshaderc_combined.a" "{target_prefix}/lib/libshaderc_combined.a"',
	# ],
	'depends_on' : ['glslang', 'spirv-headers', 'spirv-tools', 'spirv-cross', ],
	'_info' : { 'version' : None, 'fancy_name' : 'shaderc' },
}