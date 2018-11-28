{
	'repo_type' : 'git',
	'url' : 'https://github.com/kcat/openal-soft.git',
	# 'branch' : '46f18ba114831ff26e8f270c6b5c881b45838439',
	'conf_system' : 'cmake',
	# 'source_subfolder' : '_build',
	'custom_cflag' : '-O3', # native tools have to use the same march as end product else it fails*
	'configure_options':
		'. {cmake_prefix_options} -DCMAKE_TOOLCHAIN_FILE=XCompile.txt -DHOST={target_host}'
		' -DCMAKE_INSTALL_PREFIX={target_prefix} -DCMAKE_FIND_ROOT_PATH='
		' -DLIBTYPE=STATIC -DALSOFT_UTILS=OFF -DALSOFT_EXAMPLES=OFF',
	'patches' : (
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/openal/0001-versioned-w32-dll.mingw.patch', '-p1'),
		# ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/openal/0002-w32ize-portaudio-loading.mingw.patch', '-p1'),
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/openal/0003-openal-not-32.mingw.patch', '-p1'),
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/openal/0004-disable-OSS-windows.patch', '-p1'),
	),
	'run_post_patch' : [
		"sed -i.bak 's/CMAKE_INSTALL_PREFIX \"\${{CMAKE_FIND_ROOT_PATH}}\"/CMAKE_INSTALL_PREFIX ""/' XCompile.txt",
	],
	'run_post_install' : [
		"sed -i.bak 's/^Libs: -L\${{libdir}} -lopenal $/Libs: -L\${{libdir}} -lopenal -lwinmm/' '{pkg_config_path}/openal.pc'", #issue with it not using pkg-config option "--static" or so idk?
	],
	'install_options' : 'DESTDIR={target_prefix}',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'openal-soft' },
}