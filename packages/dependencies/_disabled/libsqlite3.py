{
	'repo_type' : 'archive',
	'download_locations' : [
		{ "url" : "https://www.sqlite.org/2018/sqlite-autoconf-3240000.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "d9d14e88c6fb6d68de9ca0d1f9797477d82fc3aed613558f87ffbdbbc5ceb74a" }, ], },
		{ "url" : "https://fossies.org/linux/misc/sqlite-autoconf-3240000.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "d9d14e88c6fb6d68de9ca0d1f9797477d82fc3aed613558f87ffbdbbc5ceb74a" }, ], },
	],
	'cflag_addition' : '-fexceptions -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_USE_MALLOC_H=1 -DSQLITE_USE_MSIZE=1 -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_RTREE=1 -fno-strict-aliasing',
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-threadsafe --disable-editline --enable-readline --enable-json1 --enable-fts5 --enable-session',
	'depends_on': (
		'zlib',
	),
	'_info' : { 'version' : '3.24.0', 'fancy_name' : 'libsqlite3' },
}