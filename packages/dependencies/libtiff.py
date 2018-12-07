{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://download.osgeo.org/libtiff/tiff-4.0.10.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '2c52d11ccaf767457db0c46795d9c7d1a8d8f76f68b0b800a3dfe45786b996e4' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/tiff-4.0.10.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '2c52d11ccaf767457db0c46795d9c7d1a8d8f76f68b0b800a3dfe45786b996e4' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'depends_on' : [
		'zlib','libjpeg-turbo','libwebp'
	],
	'update_check' : { 'url' : 'https://download.osgeo.org/libtiff/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'tiff-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '4.0.10', 'fancy_name' : 'libtiff' },
}