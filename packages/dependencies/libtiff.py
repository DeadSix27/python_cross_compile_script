{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://download.osgeo.org/libtiff/tiff-4.3.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '0e46e5acb087ce7d1ac53cf4f56a09b221537fc86dfc5daaad1c2e89e1b37ac8' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/tiff-4.3.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '0e46e5acb087ce7d1ac53cf4f56a09b221537fc86dfc5daaad1c2e89e1b37ac8' }, ], },
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
	'_info' : { 'version' : '4.3.0', 'fancy_name' : 'libtiff' },
}