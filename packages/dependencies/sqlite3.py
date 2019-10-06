{
	'repo_type' : 'archive',
	'custom_cflag' : '-O2', # make sure we build it without -ffast-math
	'download_locations' : [
		{ 'url' : 'https://www.sqlite.org/2019/sqlite-autoconf-3300000.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'e0a8cf4c7a87455e55e10413d16f358ca121ccec687fe1301eac95e2d340fc58' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/sqlite-autoconf-3300000.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'e0a8cf4c7a87455e55e10413d16f358ca121ccec687fe1301eac95e2d340fc58' }, ], },
	],
	'cflag_addition' : '-fexceptions -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_USE_MALLOC_H=1 -DSQLITE_USE_MSIZE=1 -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_RTREE=1 -fno-strict-aliasing',
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-threadsafe --disable-editline --enable-readline --enable-json1 --enable-fts5 --enable-session',
	'depends_on': (
		'zlib',
	),
	'update_check' : { 'url' : 'https://www.sqlite.org/index.html', 'type' : 'httpregex', 'regex' : r'<a href="releaselog/.*\.html">Version (?P<version_num>[\d.]+)<\/a>' },
	'_info' : { 'version' : '3.30.0', 'fancy_name' : 'libsqlite3' },
}