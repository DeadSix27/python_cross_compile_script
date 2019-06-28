{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://github.com/libexpat/libexpat/releases/download/R_2_2_7/expat-2.2.7.tar.bz2',	'hashes' : [ { 'type' : 'sha256', 'sum' : 'cbc9102f4a31a8dafd42d642e9a3aa31e79a0aedaa1f6efd2795ebc83174ec18' },	], },
		{ 'url' : 'https://fossies.org/linux/www/expat-2.2.7.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'cbc9102f4a31a8dafd42d642e9a3aa31e79a0aedaa1f6efd2795ebc83174ec18' }, ],	},
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
	'_info' : { 'version' : '2.2.7', 'fancy_name' : 'expat' },
}