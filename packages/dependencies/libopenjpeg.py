{
	'repo_type' : 'git',
	'url' : 'https://github.com/uclouvain/openjpeg.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS:bool=off',
	'depends_on' : [
		'zlib', 'libpng', 'libtiff', 'lcms2'
	],
	# 'patches' : [
	# 	( 'openjpeg2/use-PkgConfig-for-third-party-libraries.patch', '-p1', '..' ),
	# ],
	'_info' : { 'version' : None, 'fancy_name' : 'openjpeg' },
}