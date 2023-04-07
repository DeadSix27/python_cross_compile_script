#type:ignore
{
	'repo_type' : 'git',
	'url' : 'https://github.com/libjxl/libjxl',
	'depth_git': 0,
	'branch': 'main',
	'conf_system' : 'cmake',
	'build_system' : 'ninja',
    'patches': [
		('libjxl/0001-Fix-building-on-MinGW.patch', '-p1','..'),
    ],
	'source_subfolder' : 'build',
	'env_exports' : { # 2020.06.19
		'CFLAGS'   : ' -Wa,-muse-unaligned-vector-move {original_cflags}',
		'CXXFLAGS' : ' -Wa,-muse-unaligned-vector-move {original_cflags}',
		'CPPFLAGS' : ' -Wa,-muse-unaligned-vector-move {original_cflags}',
	},
	'run_post_patch' : [
		'!SWITCHDIR|..',
		'./deps.sh',
		'!SWITCHDIR|build',
	],
	'configure_options' : 
		'.. {cmake_prefix_options} '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} '
        '-DBUILD_SHARED_LIBS=false '
		'-DJPEGXL_ENABLE_TOOLS=false '
        '-DJPEGXL_ENABLE_JPEGLI=false '
		'-DJPEGXL_ENABLE_DOXYGEN=false '
		'-DJPEGXL_ENABLE_MANPAGES=false '
		'-DJPEGXL_ENABLE_BENCHMARK=false '
		'-DJPEGXL_ENABLE_EXAMPLES=false '
        '-DJPEGXL_ENABLE_VIEWERS=false '
        '-DJPEGXL_ENABLE_DEVTOOLS=false '
        '-DJPEGXL_ENABLE_SJPEG=false '
        '-DJPEGXL_ENABLE_JNI=false '
        '-DJPEGXL_EMSCRIPTEN=false '
        '-DJPEGXL_FORCE_SYSTEM_BROTLI=true '
        '-DJPEGXL_FORCE_SYSTEM_LCMS2=true '
        '-DJPEGXL_FORCE_SYSTEM_HWY=true '
		'-DBUILD_TESTING=false '
		'-DJPEGXL_STATIC=true '
		'-DJPEGXL_BUNDLE_LIBPNG=false'
	,
	'depends_on' : [  "brotli", "highway", "libpng", "lcms2", "libjpeg-turbo", "zlib" ],
	'update_check' : { 'type' : 'git', },
	'_info' : { 'version' : None, 'fancy_name' : 'libjxl' },
}