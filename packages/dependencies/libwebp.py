{
	'repo_type' : 'git',
	'url' : 'https://chromium.googlesource.com/webm/libwebp',
	'conf_system' : 'cmake',
	'configure_options' : '. {cmake_prefix_options} '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release'
		'-DWEBP_ENABLE_SIMD=ON '
		'-DWEBP_NEAR_LOSSLESS=ON '
		'-DWEBP_BUILD_ANIM_UTILS=OFF '
		'-DWEBP_BUILD_CWEBP=OFF '
		'-DWEBP_BUILD_DWEBP=OFF '
		'-DWEBP_BUILD_GIF2WEBP=OFF '
		'-DWEBP_BUILD_IMG2WEBP=OFF '
		'-DWEBP_BUILD_VWEBP=OFF '
		'-DWEBP_BUILD_WEBPINFO=OFF '
		'-DWEBP_BUILD_WEBPMUX=OFF '
		'-DWEBP_BUILD_EXTRAS=OFF '
		'-DWEBP_UNICODE=OFF '
		'-DWEBP_BUILD_WEBP_JS=OFF '
	,
	'depends_on' : [ 'libpng', 'libjpeg-turbo' ],
	'_info' : { 'version' : None, 'fancy_name' : 'libwebp' },
}