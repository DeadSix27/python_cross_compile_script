{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://download.osgeo.org/libtiff/tiff-4.5.0.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'dafac979c5e7b6c650025569c5a4e720995ba5f17bc17e6276d1f12427be267c' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/tiff-4.5.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'dafac979c5e7b6c650025569c5a4e720995ba5f17bc17e6276d1f12427be267c' }, ], },
	],
	#'custom_cflag' : '-O3',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -Dtiff-tools=OFF -Dtiff-docs=OFF -Dtiff-contrib=OFF -Dtiff-tests=OFF -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DCMAKE_BUILD_TYPE=Release',
    'patches' : [
		# ('tiff1.patch', '-p1', ".."),
	],
	'regex_replace': {
		'post_install': [
			{
				0: r'Libs: -L[^\n]+',
				1: r'Libs: -L${{libdir}} -ltiff -lwebp -llzma -ljpeg -lz',
				'in_file': '{pkg_config_path}/libtiff-4.pc'
			}
		]
	},
	'depends_on' : [
		'zlib', 'libjpeg-turbo', 'libwebp'
	],
	'update_check' : { 'url' : 'https://download.osgeo.org/libtiff/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'tiff-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '4.5.0', 'fancy_name' : 'libtiff' },
}