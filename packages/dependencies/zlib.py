{
	'repo_type' : 'git',
	'url' : 'https://github.com/madler/zlib.git',
	'env_exports' : {
		'AR' : '{cross_prefix_bare}ar',
		'CC' : '{cross_prefix_bare}gcc',
		'PREFIX' : '{target_prefix}',
		'RANLIB' : '{cross_prefix_bare}ranlib',
		'LD'     : '{cross_prefix_bare}ld',
		'STRIP'  : '{cross_prefix_bare}strip',
		'CXX'    : '{cross_prefix_bare}g++',
	},
	'configure_options' : '--static --prefix={target_prefix}',
	'build_options' : '{make_prefix_options} ARFLAGS=rcs',
	'_info' : { 'version' : None, 'fancy_name' : 'zlib' },
}