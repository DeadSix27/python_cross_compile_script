{
	'repo_type' : 'git',
	'url' : 'https://github.com/OpenMPT/openmpt.git',
	# 'source_subfolder' : '_build',
	'needs_configure' : False,
	'build_options' : '{make_prefix_options} VERBOSE=1 TEST=0 SHARED_LIB=0 SHARED_SONAME=0 DYNLINK=0 STATIC_LIB=1 EXAMPLES=0 MODERN=1',
	'install_options' : '{make_prefix_options} uVERBOSE=1 TEST=0 SHARED_LIB=0 SHARED_SONAME=0 DYNLINK=0 STATIC_LIB=1 EXAMPLES=0 MODERN=1 PREFIX={target_prefix}',
	# 'configure_path' : '../build/autotools/configure',
	# 'run_post_patch' : [
		# '!SWITCHDIR|../build/autotools',
		# 'autoreconf -fiv',
		# '!SWITCHDIR|../../_build',
	# ],
	# 'configure_options' : '--prefix={target_prefix} --host={target_host}',

	'run_post_patch' : [
		'cp -fv {cross_prefix_full}ld {mingw_binpath}/ld',
	],
	'run_post_install' : [
		'rm -v {mingw_binpath}/ld',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'openmpt' },
}