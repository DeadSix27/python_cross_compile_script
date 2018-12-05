{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://sourceforge.net/projects/libpng/files/libpng16/1.6.36/libpng-1.6.36.tar.xz',	'hashes' : [ { 'type' : 'sha256', 'sum' : 'eceb924c1fa6b79172fdfd008d335f0e59172a86a66481e09d4089df872aa319' },	], },
		{ 'url' : 'https://fossies.org/linux/misc/libpng-1.6.36.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'eceb924c1fa6b79172fdfd008d335f0e59172a86a66481e09d4089df872aa319' }, ],	},
	],
	# 'custom_cflag' : '-fno-asynchronous-unwind-tables',
	'conf_system' : 'cmake',
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DBUILD_BINARY=OFF -DCMAKE_BUILD_TYPE=Release -DPNG_TESTS=OFF -DPNG_SHARED=OFF -DPNG_STATIC=ON',
	# 'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --oldincludedir={target_prefix}/include',
	'patches' : [
		('libpng/libpng-1.6.36-apng.patch', '-p1'),
	],
	'depends_on' : [ 'zlib', ],
	'update_check' : { 'url' : 'https://sourceforge.net/projects/libpng/files/libpng16/', 'type' : 'sourceforge', },
	'_info' : { 'version' : '1.6.36', 'fancy_name' : 'libpng' },
}