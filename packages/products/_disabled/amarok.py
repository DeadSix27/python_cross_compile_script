{
	'repo_type' : 'git',
	'url' : 'git://anongit.kde.org/amarok.git',
	'needs_make_install':False,
	'conf_system' : 'cmake',
	'configure_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix}',
	# 'custom_cflag' : '-DTAGLIB_STATIC',
	'env_exports' : {
		'CPPDEFINES' : '-DTAGLIB_STATIC',
		# build.env.Append(CPPDEFINES = 'TAGLIB_STATIC')
	},
	'depends_on': [
		'taglib',
	],
}