{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://github.com/libexpat/libexpat/releases/download/R_2_2_6/expat-2.2.6.tar.bz2',	'hashes' : [ { 'type' : 'sha256', 'sum' : '17b43c2716d521369f82fc2dc70f359860e90fa440bea65b3b85f0b246ea81f2' },	], },
		{ 'url' : 'https://fossies.org/linux/www/expat-2.2.6.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '17b43c2716d521369f82fc2dc70f359860e90fa440bea65b3b85f0b246ea81f2' }, ],	},
	],
	'env_exports' : {
		'CPPFLAGS' : '-DXML_LARGE_SIZE',
	},
	'run_post_patch' : [
		'sed -i.bak "s/SUBDIRS += xmlwf doc/SUBDIRS += xmlwf/" Makefile.am',
		'aclocal',
		'automake',
	],
	'update_check_url' : { 'url' : 'https://github.com/libexpat/libexpat/releases', 'type' : 'githubreleases', 'name_or_tag' : 'name' },
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --without-docbook',
	'_info' : { 'version' : '2.2.6', 'fancy_name' : 'expat' },
}