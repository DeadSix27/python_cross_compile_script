{
	'repo_type' : 'git',
	'url' : 'https://github.com/DanBloomberg/leptonica.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'depends_on' : [ 'zlib', 'libopenjpeg', 'libpng', 'libwebp', 'libjpeg-turbo', 'dlfcn-win32' ],
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DSTATIC=1 -DLIBRARY_TYPE=STATIC -DCMAKE_BUILD_TYPE=Release',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'tesseract' },
}
#TODO: Add GIF/TIFF Library?