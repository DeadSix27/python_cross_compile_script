{
	'repo_type' : 'git',
	'url' : 'https://github.com/clementine-player/Clementine.git',
	'needs_make_install':False,
	'conf_system' : 'cmake',
	'configure_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF',
	'depends_on': [
		'qt4',
	],
	'_disabled': True,
}