{
	'repo_type' : 'git',
	'url' : 'https://github.com/breakfastquay/rubberband.git',
	'download_header' : [
		'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/additional_headers/ladspa.h',
	],
	'env_exports' : {
		'AR' : '{cross_prefix_bare}ar',
		'CC' : '{cross_prefix_bare}gcc',
		'PREFIX' : '{target_prefix}',
		'RANLIB' : '{cross_prefix_bare}ranlib',
		'LD'     : '{cross_prefix_bare}ld',
		'STRIP'  : '{cross_prefix_bare}strip',
		'CXX'    : '{cross_prefix_bare}g++',
	},
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'build_options' : '{make_prefix_options}',
	'needs_make_install' : False,
	'run_post_build' : [
		'cp -fv lib/* "{target_prefix}/lib"',
		'cp -frv rubberband "{target_prefix}/include"',
		'cp -fv rubberband.pc.in "{pkg_config_path}/rubberband.pc"',
		'sed -i.bak "s|%PREFIX%|{target_prefix_sed_escaped}|" "{pkg_config_path}/rubberband.pc"',
		'sed -i.bak \'s/-lrubberband *$/-lrubberband -lfftw3 -lsamplerate -lstdc++/\' "{pkg_config_path}/rubberband.pc"',
	],
	'depends_on' : [
		'libsndfile',
	],
	'_info' : { 'version' : '1.8.1', 'fancy_name' : 'librubberband' },
}