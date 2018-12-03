{
	'repo_type' : 'git',
	'url' : 'https://github.com/google/shaderc.git',
	'configure_options': 'cmake .. {cmake_prefix_options} -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=cmake/linux-mingw-toolchain.cmake -DCMAKE_INSTALL_PREFIX={target_prefix} -DSHADERC_SKIP_INSTALL=ON -DSHADERC_SKIP_TESTS=ON -DMINGW_COMPILER_PREFIX={cross_prefix_bare}', #-DCMAKE_CXX_FLAGS="${{CMAKE_CXX_FLAGS}} -fno-rtti"
	'source_subfolder' : '_build', #-B. -H..
	'conf_system' : 'cmake',
	# 'cpu_count' : '1', #...
	'needs_make_install' : False,
	'build_options': '',
	# 'patches' : [
		# ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/shaderc/shaderc-0001-add-script-for-cloning-dependencies.patch', '-p1', '..'),
	# ],
	'run_post_patch' : [
		# 'mkdir _build',
		# 'chmod u+x pull.sh',
		# './pull.sh',
		'!SWITCHDIR|../third_party',
		'ln -sf {inTreePrefix}/glslang/ glslang',
		'ln -sf {inTreePrefix}/spirv-headers/ spirv-headers',
		'ln -sf {inTreePrefix}/spirv-tools/ spirv-tools',
		'!SWITCHDIR|../_build',
		"sed -i 's/add_subdirectory(examples)/#add_subdirectory(examples)/g' ../CMakeLists.txt",
		'mkdir -p third_party',
		'!SWITCHDIR|third_party',
		'ln -sf {inTreePrefix}/glslang glslang',
		'ln -sf {inTreePrefix}/spirv-headers spirv-headers',
		'ln -sf {inTreePrefix}/spirv-tools spirv-tools',
		'!SWITCHDIR|..',
	],
	'run_post_build' : (
		'cp -rv "../libshaderc/include/shaderc" "{target_prefix}/include/"',
		'cp -rv "libshaderc/libshaderc_combined.a" "{target_prefix}/lib/libshaderc_combined.a"',
		'cp -rv "libshaderc/libshaderc_combined.a" "{target_prefix}/lib/libshaderc_shared.a"',
	),
	'depends_on' : ['glslang', 'spirv_headers', 'spirv_tools', 'crossc'],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'shaderc' },
}