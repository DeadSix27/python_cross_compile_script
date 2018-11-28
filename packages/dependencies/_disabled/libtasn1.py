{
	'repo_type' : 'archive',
	'url' : 'https://ftp.gnu.org/gnu/libtasn1/libtasn1-4.13.tar.gz',
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-doc',
	'run_post_patch' : [
		'autoreconf -fiv',
	],
	'_info' : { 'version' : '4.13', 'fancy_name' : 'libtasn1' },
}