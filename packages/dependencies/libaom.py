{
	'repo_type' : 'git',
	'url' : 'https://aomedia.googlesource.com/aom',
	'branch' : '9284af62c37d62117c007d100e0442f144220ab8',
	'conf_system' : 'cmake',
	'source_subfolder' : 'build',
	'configure_options': '.. {cmake_prefix_options} '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} '
		'-DCONFIG_LOWBITDEPTH=0 -DCONFIG_HIGHBITDEPTH=1 '
		'-DCONFIG_AV1=1 -DHAVE_PTHREAD=1 -DBUILD_SHARED_LIBS=0 -DENABLE_DOCS=0 -DCONFIG_INSTALL_DOCS=0 '
		'-DCONFIG_INSTALL_BINS=0 -DCONFIG_INSTALL_LIBS=1 '
		'-DCONFIG_INSTALL_SRCS=1 -DCONFIG_UNIT_TESTS=0 -DENABLE_TESTS=0 -DENABLE_TESTDATA=0 '
		'-DCONFIG_AV1_DECODER=1 -DCONFIG_AV1_ENCODER=1 '
		'-DCONFIG_MULTITHREAD=1 -DCONFIG_PIC=1 -DCONFIG_COEFFICIENT_RANGE_CHECKING=0 '
		'-DCONFIG_RUNTIME_CPU_DETECT=1 -DCONFIG_WEBM_IO=1 '
		'-DCONFIG_SPATIAL_RESAMPLING=1 -DENABLE_NASM=off '
		'-DLIBXML_STATIC=1 -DGLIB_STATIC_COMPILATION=1'
	,
	'depends_on' : [ 'libxml2' ],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libaom' },
}