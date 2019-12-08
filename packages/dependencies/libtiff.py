{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://download.osgeo.org/libtiff/tiff-4.1.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '5d29f32517dadb6dbcd1255ea5bbc93a2b54b94fbf83653b4d65c7d6775b8634' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/tiff-4.1.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '5d29f32517dadb6dbcd1255ea5bbc93a2b54b94fbf83653b4d65c7d6775b8634' }, ], },
	],
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DCMAKE_BUILD_TYPE=Release',
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
	'_info' : { 'version' : '4.1.0', 'fancy_name' : 'libtiff' },
}