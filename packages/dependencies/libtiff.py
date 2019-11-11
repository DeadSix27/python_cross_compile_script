{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://download.osgeo.org/libtiff/tiff-4.1.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '5d29f32517dadb6dbcd1255ea5bbc93a2b54b94fbf83653b4d65c7d6775b8634' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/tiff-4.1.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '5d29f32517dadb6dbcd1255ea5bbc93a2b54b94fbf83653b4d65c7d6775b8634' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'depends_on' : [
		'zlib','libjpeg-turbo','libwebp'
	],
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -ltiff$/Libs: -L${{libdir}} -ltiff -lwebp -llzma -ljpeg -lz/\' "{pkg_config_path}/libtiff-4.pc"',
	],
	'update_check' : { 'url' : 'https://download.osgeo.org/libtiff/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'tiff-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '4.1.0', 'fancy_name' : 'libtiff' },
}