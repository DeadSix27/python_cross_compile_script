{
	'repo_type' : 'git',
	'url' : 'https://github.com/DeadSix27/python_mingw_libs.git',
	'needs_configure' : False,
	'needs_make_install' : False,
	'build_options' : 'PREFIX={target_prefix} PYTHON_VERSION=3.11.2 GENDEF={mingw_binpath}/gendef DLLTOOL={mingw_binpath}/{cross_prefix_bare}dlltool',
	'_info' : { 'version' : '3.11.2', 'fancy_name' : 'Python (library-only)' },
}