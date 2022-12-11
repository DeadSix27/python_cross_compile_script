{
	'repo_type' : 'git',
	'url' : 'https://github.com/erikd/libsndfile.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	#'custom_cflag' : '-O3',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DBUILD_PROGRAMS=OFF -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF -DENABLE_BOW_DOCS=OFF -DENABLE_STATIC_RUNTIME=ON -DCMAKE_BUILD_TYPE=Release',
	'depends_on' : [ 'libogg', 'libvorbis', 'libflac', 'libsamplerate', 'libopus', 'libspeex' ],
	# 'run_post_install' : [ # -lspeex
	# 	'sed -i.bak \'s/Libs: -L${{libdir}} -lsndfile/Libs: -L${{libdir}} -lsndfile -lopus -lFLAC -lvorbis -lvorbisenc -logg/\' "{pkg_config_path}/sndfile.pc"',  # -lssp
	# ],
    
	'env_exports' : { # 2020.06.19
		'CFLAGS'   : ' -DFLAC__NO_DLL {original_cflags}',
		'CXXFLAGS' : ' -DFLAC__NO_DLL {original_cflags}',
		'CPPFLAGS' : ' -DFLAC__NO_DLL {original_cflags}', # 2020.06.20 per https://github.com/fribidi/fribidi/issues/146#issuecomment-646991416
		'LDFLAGS'  : ' -DFLAC__NO_DLL {original_cflags}',
	},

	'regex_replace': {
		'post_install': [
			{
				0: r'^Requires:([\n\r\s]+)?$',
				1: r'Requires: opus flac vorbis vorbisenc ogg speex\1',
				'in_file': '{pkg_config_path}/sndfile.pc'
			},
		],
	},

	'_info' : { 'version' : None, 'fancy_name' : 'libsndfile' },
}