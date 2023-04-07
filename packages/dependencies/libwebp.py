#type: ignore
{
	'repo_type' : 'git',
	'url' : 'https://chromium.googlesource.com/webm/libwebp',
	'branch': 'main',
	'source_subfolder': '_build',
	'conf_system' : 'cmake',
	#'custom_cflag' : '-O3',
	'configure_options' : '.. {cmake_prefix_options} '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} -DConfigPackageLocation={target_prefix}/lib/cmake/WebP/ -DBUILD_SHARED_LIBS=OFF -DWEBP_BUILD_EXTRAS=OFF'
		'-DWEBP_ENABLE_SIMD=ON '
		'-DWEBP_NEAR_LOSSLESS=ON '
		'-DWEBP_UNICODE=ON '

		'-DWEBP_BUILD_GIF2WEBP=OFF '
		'-DWEBP_BUILD_IMG2WEBP=OFF '
		'-DWEBP_BUILD_WEBPMUX=OFF '
		'-DWEBP_BUILD_ANIM_UTILS=OFF '
		'-DWEBP_BUILD_CWEBP=OFF '
		'-DWEBP_BUILD_DWEBP=OFF '
		'-DWEBP_BUILD_VWEBP=OFF '
		'-DWEBP_BUILD_WEBPINFO=OFF '
		'-DWEBP_BUILD_EXTRAS=0 '
		'-DWEBP_BUILD_WEBP_JS=OFF -DCMAKE_BUILD_TYPE=Release'
	,
	'regex_replace': {
		'post_patch': [
			{
				# for some silly reason they only build libwebpmux when these variables are set ON,
				# however if they're on it will also build the binary CLI tools IMG2WEBP.exe and GIF2WEBP.exe,
				# which we do not want or need... so this hack exists.
				#
				# Note: Probably warrants a pull-request, maybe later.
				#
				0: r'if\(WEBP_BUILD_GIF2WEBP OR WEBP_BUILD_IMG2WEBP\)',
				1: r'if(MINGW)',
				'in_file': '../CMakeLists.txt'
			},
		],
	},
	'depends_on' : [ 'libpng', 'libjpeg-turbo' ],
	'_info' : { 'version' : None, 'fancy_name' : 'libwebp' },
}