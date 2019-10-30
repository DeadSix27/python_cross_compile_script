{
	'repo_type' : 'git',
	'url' : 'https://github.com/erikd/libsndfile.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DBUILD_PROGRAMS=OFF -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF -DENABLE_BOW_DOCS=OFF -DENABLE_STATIC_RUNTIME=ON -DCMAKE_BUILD_TYPE=Release',
	'depends_on' : [ 'libspeex' ],
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lsndfile/Libs: -L${{libdir}} -lsndfile -lopus -lFLAC -lvorbis -lvorbisenc -logg -lspeex/\' "{pkg_config_path}/sndfile.pc"', 
	],
	'_info' : { 'version' : None, 'fancy_name' : 'libsndfile' },
}