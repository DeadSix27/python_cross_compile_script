{
	'repo_type' : 'git',
	'url' : 'https://github.com/DanBloomberg/leptonica.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'env_exports' : {
		'CPPFLAGS' : '-DOPJ_STATIC',
		'CFLAGS' : '-DOPJ_STATIC'
	},
	'run_post_patch' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -l@leptonica_NAME@/Libs: -L${{libdir}} -l@leptonica_NAME@-@leptonica_VERSION@/\' ../lept.pc.cmake',
	],
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} /Requires: libtiff-4 libpng libopenjp2 libjpeg libwebp\\nRequires.private: libtiff-4 libpng libopenjp2 libjpeg libwebp\\nLibs: -L${{libdir}} /\' "{pkg_config_path}/lept.pc"',
		'sed -i \'s/Libs: -L${{libdir}} -lleptonica-\(.*\)$/Libs: -L${{libdir}} -lleptonica-\\1 -lgif/\' "{pkg_config_path}/lept.pc"',
	],
	'depends_on' : [ 'zlib', 'libopenjpeg', 'libpng', 'libwebp', 'dlfcn-win32', 'libjpeg-turbo', 'giflib', 'libtiff', ],
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DSW_BUILD=0 -DBUILD_PROG=0 -DBUILD_SHARED_LIBS=0 -DSTATIC=1 -DLIBRARY_TYPE=STATIC -DCMAKE_BUILD_TYPE=Release',
	'_info' : { 'version' : None, 'fancy_name' : 'tesseract' },
}
#TODO: Add GIF/TIFF Library?