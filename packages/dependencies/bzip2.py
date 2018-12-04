{
	'repo_type' : 'archive',
	'download_locations' : [
		#{ 'url' : 'http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'a2848f34fcd5d6cf47def00461fcb528a0484d8edef8208d6d2e2909dc61d9cd' }, ], }, # Website is dead.
		{ 'url' : 'https://fossies.org/linux/misc/bzip2-1.0.6.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'a2848f34fcd5d6cf47def00461fcb528a0484d8edef8208d6d2e2909dc61d9cd' }, ], },
	],
	'patches' : [
		('bzip2/bzip2_cross_compile.diff', '-p0'),
		('bzip2/bzip2-1.0.6-gcc8.patch', '-p0'),
	],
	'needs_configure' : False,
	'needs_make' : True,
	'needs_make_install' : False,
	'build_options' : '{make_prefix_options} libbz2.a bzip2 bzip2recover install',
	'_info' : { 'version' : '1.0.6', 'fancy_name' : 'BZip2 (library)' },
}