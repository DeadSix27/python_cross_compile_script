{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: https://sourceforge.net/projects/freetype/files/freetype2/
		{ "url" : "https://fossies.org/linux/misc/freetype-2.9.1.tar.bz2", "hashes" : [ { "type" : "sha256", "sum" : "db8d87ea720ea9d5edc5388fc7a0497bb11ba9fe972245e0f7f4c7e8b1e1e84d" }, ], },
		{ "url" : "https://sourceforge.net/projects/freetype/files/freetype2/2.9.1/freetype-2.9.1.tar.bz2", "hashes" : [ { "type" : "sha256", "sum" : "db8d87ea720ea9d5edc5388fc7a0497bb11ba9fe972245e0f7f4c7e8b1e1e84d" }, ], },
	],
	'configure_options': '--host={target_host} --build=x86_64-linux-gnu --prefix={target_prefix} --disable-shared --enable-static --with-zlib={target_prefix} --without-png --with-harfbuzz=no',
	'_info' : { 'version' : '2.9.1', 'fancy_name' : 'freetype2' },
}