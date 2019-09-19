{
	'repo_type' : 'git',
	'url' : 'https://github.com/erikd/libsndfile.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-sqlite --disable-test-coverage --enable-external-libs --enable-experimental',
	'run_post_patch' : [
		'autoreconf -fiv -I M4',
	],
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lsndfile/Libs: -L${{libdir}} -lsndfile -lFLAC -lvorbis -lvorbisenc -logg -lspeex/\' "{pkg_config_path}/sndfile.pc"', #issue with rubberband not using pkg-config option "--static" or so idk?
	],
	'cflag_addition': '-D_FORTIFY_SOURCE=0',
	'depends_on' : [ 'libspeex' ],
	'packages' : {
		'arch' : [ 'autogen' ],
	},
	'_info' : { 'version' : None, 'fancy_name' : 'libsndfile' },
}