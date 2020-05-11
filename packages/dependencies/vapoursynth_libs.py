{
	'repo_type' : 'git',
	'url' : 'https://github.com/DeadSix27/vapoursynth_mingw_libs.git',
	'needs_configure' : False,
	'needs_make_install' : False,
	'depends_on' : [ 'python3_libs' ],
	'build_options' : 'PREFIX={target_prefix} GENDEF={mingw_binpath}/gendef DLLTOOL={mingw_binpath}/{cross_prefix_bare}dlltool',
	'packages' : {
		'arch' : [ '7za' ],
	},
	'_info' : { 'version' : 'R49', 'fancy_name' : 'VapourSynth (library-only)' },
}