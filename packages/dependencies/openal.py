{
	'repo_type' : 'git',
	'url' : 'https://github.com/kcat/openal-soft.git',
	# 'branch' : '0f24139b57460c71d66b9a090217d34706d64dde', # stick to last working commit
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'custom_cflag' : '-O3', # native tools have to use the same march as end product else it fails*
	'configure_options' :
		'.. {cmake_prefix_options} -DCMAKE_TOOLCHAIN_FILE=XCompile.txt -DHOST={target_host}'
		' -DCMAKE_INSTALL_PREFIX={target_prefix} -DCMAKE_FIND_ROOT_PATH='
		' -DLIBTYPE=STATIC -DALSOFT_UTILS=OFF -DALSOFT_EXAMPLES=OFF',
	'patches' : [
		('openal/0001-versioned-w32-dll.mingw.patch', '-p1','..'),
		# ('openal/0002-w32ize-portaudio-loading.mingw.patch', '-p1'),
		('openal/0003-openal-not-32.mingw.patch', '-p1','..'),
		('openal/0004-disable-OSS-windows.patch', '-p1','..'),
	],
	'run_post_patch' : [
		"sed -i.bak 's/CMAKE_INSTALL_PREFIX \"\${{CMAKE_FIND_ROOT_PATH}}\"/CMAKE_INSTALL_PREFIX ""/' ../XCompile.txt",
		"sed -i.bak 's/FIND_PACKAGE(DSound)/OPTION(ALSOFT_BACKEND_DSOUND \"Enable DirectSound backend\" ON)\\nSET(HAVE_DSOUND 1)\\nSET(BACKENDS  \"${{BACKENDS}} DirectSound${{IS_LINKED}},\")\\nSET(ALC_OBJS  ${{ALC_OBJS}} Alc\/backends\/dsound.cpp Alc\/backends\/dsound.h)/g' ../CMakeLists.txt",
	],
	'run_post_install' : [
		"sed -i.bak 's/^Libs: -L\${{libdir}} -lopenal $/Libs: -L\${{libdir}} -lopenal -lwinmm/' '{pkg_config_path}/openal.pc'", #issue with it not using pkg-config option "--static" or so idk?
	],
	'install_options' : 'DESTDIR={target_prefix}',
	'_info' : { 'version' : None, 'fancy_name' : 'openal-soft' },
}