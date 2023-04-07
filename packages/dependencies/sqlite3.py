{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://www.sqlite.org/2022/sqlite-autoconf-3400100.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '2c5dea207fa508d765af1ef620b637dcb06572afa6f01f0815bd5bbf864b33d9' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/sqlite-autoconf-3400100.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '2c5dea207fa508d765af1ef620b637dcb06572afa6f01f0815bd5bbf864b33d9' }, ], },
	],
	'cflag_addition' : '-fexceptions -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_USE_MALLOC_H=1 -DSQLITE_USE_MSIZE=1 -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_RTREE=1 -fno-strict-aliasing',
	'strip_cflags': ['-ffast-math', ],
	'configure_options': '{autoconf_prefix_options} --enable-threadsafe --disable-editline --enable-readline --enable-json1 --enable-fts5 --enable-session',
	'depends_on': (
		'zlib',
	),
	'update_check' : { 'url' : 'https://www.sqlite.org/index.html', 'type' : 'httpregex', 'regex' : r'<a href="releaselog/.*\.html">Version (?P<version_num>[\d.]+)<\/a>' },
	'_info' : { 'version' : '3.40.1', 'fancy_name' : 'libsqlite3' },
}