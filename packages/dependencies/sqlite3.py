{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://www.sqlite.org/2021/sqlite-autoconf-3360000.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'bd90c3eb96bee996206b83be7065c9ce19aef38c3f4fb53073ada0d0b69bbce3' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/sqlite-autoconf-3360000.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'bd90c3eb96bee996206b83be7065c9ce19aef38c3f4fb53073ada0d0b69bbce3' }, ], },
	],
	'cflag_addition' : '-fexceptions -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_USE_MALLOC_H=1 -DSQLITE_USE_MSIZE=1 -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_RTREE=1 -fno-strict-aliasing',
	'strip_cflags': ['-ffast-math', ],
	'configure_options': '{autoconf_prefix_options} --enable-threadsafe --disable-editline --enable-readline --enable-json1 --enable-fts5 --enable-session',
	'depends_on': (
		'zlib',
	),
	'update_check' : { 'url' : 'https://www.sqlite.org/index.html', 'type' : 'httpregex', 'regex' : r'<a href="releaselog/.*\.html">Version (?P<version_num>[\d.]+)<\/a>' },
	'_info' : { 'version' : '3.36.0', 'fancy_name' : 'libsqlite3' },
}