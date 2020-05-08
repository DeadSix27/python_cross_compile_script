{
	'repo_type' : 'git',
	'url' : 'https://aomedia.googlesource.com/aom',
	'depth_git': 0,
	'branch': 'v2.0.0-rc1',
	'conf_system' : 'cmake',
	'source_subfolder' : 'build',
	'configure_options' : 
		'.. {cmake_prefix_options} '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} '
		'-DBUILD_SHARED_LIBS=0 '
		'-DENABLE_DOCS=0 '
		'-DENABLE_TESTS=0 '
		'-DENABLE_TOOLS=0 '
		'-DENABLE_CCACHE=1 '
		'-DCONFIG_LPF_MASK=1 '
		'-DENABLE_EXAMPLES=0 '
		'-DENABLE_TESTDATA=0 '
		'-DCONFIG_AV1_DECODER=1 '
		'-DCONFIG_AV1_ENCODER=1 '
		'-DCONFIG_PIC=1 '
		'-DCONFIG_SPATIAL_RESAMPLING=1 '
		'-DENABLE_NASM=off ' # YASM is preferred (default)
		'-DCONFIG_STATIC=1 '
		'-DCONFIG_SHARED=0'
	,
	'depends_on' : [ 'libxml2' ],
	'update_check' : { 'type' : 'git', },
	'_info' : { 'version' : None, 'fancy_name' : 'libaom' },
}