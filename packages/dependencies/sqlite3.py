{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://www.sqlite.org/2020/sqlite-autoconf-3310100.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '62284efebc05a76f909c580ffa5c008a7d22a1287285d68b7825a2b6b51949ae' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/sqlite-autoconf-3310100.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '62284efebc05a76f909c580ffa5c008a7d22a1287285d68b7825a2b6b51949ae' }, ], },
	],
	'cflag_addition' : '-fexceptions -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_USE_MALLOC_H=1 -DSQLITE_USE_MSIZE=1 -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_RTREE=1 -fno-strict-aliasing',
	'strip_cflags': ['-ffast-math', ],
	'configure_options': '{autoconf_prefix_options} --enable-threadsafe --disable-editline --enable-readline --enable-json1 --enable-fts5 --enable-session',
	'depends_on': (
		'zlib',
	),
	'update_check' : { 'url' : 'https://www.sqlite.org/index.html', 'type' : 'httpregex', 'regex' : r'<a href="releaselog/.*\.html">Version (?P<version_num>[\d.]+)<\/a>' },
	'_info' : { 'version' : '3.31.1', 'fancy_name' : 'libsqlite3' },
}