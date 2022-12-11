{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://sourceforge.net/projects/libpng/files/libpng16/1.6.39/libpng-1.6.39.tar.xz',	'hashes' : [ { 'type' : 'sha256', 'sum' : '1f4696ce70b4ee5f85f1e1623dc1229b210029fa4b7aee573df3e2ba7b036937' },	], },
		{ 'url' : 'https://fossies.org/linux/misc/libpng-1.6.39.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '1f4696ce70b4ee5f85f1e1623dc1229b210029fa4b7aee573df3e2ba7b036937' }, ],	},
	],
	# 'custom_cflag' : '-fno-asynchronous-unwind-tables',
	'conf_system' : 'cmake',
	#'custom_cflag' : '-O3',
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release -DPNG_TESTS=OFF -DPNG_SHARED=OFF -DPNG_STATIC=ON',
	'patches' : [
		('libpng/libpng-1.6.39-apng.patch', '-p1'),
	],
	'depends_on' : [ 'zlib', ],
	'update_check' : { 'url' : 'https://sourceforge.net/projects/libpng/files/libpng16/', 'type' : 'sourceforge', },
	'_info' : { 'version' : '1.6.38', 'fancy_name' : 'libpng' },
}