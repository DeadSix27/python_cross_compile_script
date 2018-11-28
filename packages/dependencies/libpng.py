{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: https://sourceforge.net/projects/libpng/files/libpng16/
		{ "url" : "https://sourceforge.net/projects/libpng/files/libpng16/1.6.35/libpng-1.6.35.tar.xz",	"hashes" : [ { "type" : "sha256", "sum" : "23912ec8c9584917ed9b09c5023465d71709dce089be503c7867fec68a93bcd7" },	], },
		{ "url" : "https://fossies.org/linux/misc/libpng-1.6.35.tar.xz", "hashes" : [ { "type" : "sha256", "sum" : "23912ec8c9584917ed9b09c5023465d71709dce089be503c7867fec68a93bcd7" }, ],	},
	],
	# 'custom_cflag' : '-fno-asynchronous-unwind-tables',
	'conf_system' : 'cmake',
	'configure_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DBUILD_BINARY=OFF -DCMAKE_BUILD_TYPE=Release -DPNG_TESTS=OFF -DPNG_SHARED=OFF -DPNG_STATIC=ON',
	# 'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --oldincludedir={target_prefix}/include',
	'patches' : [
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libpng/libpng-1.6.35-apng.patch', '-p1'),
	],
	'depends_on' : [ 'zlib', ],
	'_info' : { 'version' : '1.6.35', 'fancy_name' : 'libpng' },
}