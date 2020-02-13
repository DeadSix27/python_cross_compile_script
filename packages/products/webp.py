{
	'repo_type' : 'git',
	'url' : 'https://chromium.googlesource.com/webm/libwebp',
	'source_subfolder': '_build',
	'conf_system' : 'cmake',
	'configure_options' : '.. {cmake_prefix_options} '
		'-DCMAKE_INSTALL_PREFIX={output_prefix}/webp.installed -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release'
		'-DWEBP_ENABLE_SIMD=ON '
		'-DWEBP_NEAR_LOSSLESS=ON '
		'-DWEBP_UNICODE=ON '

		'-DWEBP_BUILD_GIF2WEBP=OFF '
		'-DWEBP_BUILD_IMG2WEBP=OFF '
		'-DWEBP_BUILD_WEBPMUX=OFF '
		'-DWEBP_BUILD_ANIM_UTILS=OFF '
		'-DWEBP_BUILD_CWEBP=ON '
		'-DWEBP_BUILD_DWEBP=ON '
		'-DWEBP_BUILD_VWEBP=ON '
		'-DWEBP_BUILD_WEBPINFO=ON '
		'-DWEBP_BUILD_EXTRAS=OFF '
		'-DWEBP_BUILD_WEBP_JS=OFF '
	,
	'depends_on' : [ 'libpng', 'libjpeg-turbo' ],
	'_info' : { 'version' : None, 'fancy_name' : 'webp' },
}