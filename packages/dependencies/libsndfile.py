{
	'repo_type' : 'git',
	#'branch' : '81a71e08c09b20b0255aa66e40fce293008b9525', # 'd2ca7f4afc776d7c0c14c9a9a5ba94d9ae3affb8',
	'url' : 'https://github.com/erikd/libsndfile.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-sqlite --disable-test-coverage --enable-external-libs --enable-experimental',
	#'patches' : [ #patches courtesy of https://github.com/Alexpux/MINGW-packages/tree/master/mingw-w64-libsndfile
		#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libsndfile/0001-more-elegant-and-foolproof-autogen-fallback.all.patch', '-p0'),
		#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libsndfile/0003-fix-source-searches.mingw.patch', '-p0'),
	#],
	'run_post_patch' : [
		'autoreconf -fiv -I M4',
	],
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lsndfile/Libs: -L${{libdir}} -lsndfile -lFLAC -lvorbis -lvorbisenc -logg -lspeex/\' "{pkg_config_path}/sndfile.pc"', #issue with rubberband not using pkg-config option "--static" or so idk?
	],
	'depends_on' : [	'libspeex' ],
	'packages' : {
		'arch' : [ 'autogen' ],
	},
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libsndfile' },
}