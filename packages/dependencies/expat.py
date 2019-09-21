{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://github.com/libexpat/libexpat/releases/download/R_2_2_8/expat-2.2.8.tar.xz',	'hashes' : [ { 'type' : 'sha256', 'sum' : '61caa81a49d858afb2031c7b1a25c97174e7f2009aa1ec4e1ffad2316b91779b' },	], },
		{ 'url' : 'https://fossies.org/linux/www/expat-2.2.8.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '61caa81a49d858afb2031c7b1a25c97174e7f2009aa1ec4e1ffad2316b91779b' }, ],	},
	],
	'env_exports' : {
		'CPPFLAGS' : '-DXML_LARGE_SIZE',
	},
	'run_post_patch' : [
		'sed -i.bak "s/SUBDIRS += xmlwf doc/SUBDIRS += xmlwf/" Makefile.am',
		'aclocal',
		'automake',
	],
	'update_check' : { 'url' : 'https://github.com/libexpat/libexpat/releases', 'type' : 'githubreleases', 'name_or_tag' : 'name' },
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --without-docbook',
	'_info' : { 'version' : '2.2.8', 'fancy_name' : 'expat' },
}