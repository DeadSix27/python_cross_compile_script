{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://www.lysator.liu.se/~nisse/archive/nettle-3.4.1rc1.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '5a380e9a7b5e4dde2c1aff4de090ed365500046c7c24c2de06933ed09262c1b5' }, ], },
	],
	'folder_name' : 'nettle-3.4.1',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-openssl --with-included-libtasn1',
	'depends_on' : [
		'gmp',
	],
	'update_check' : { 'url' : 'https://ftp.gnu.org/gnu/nettle/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'nettle-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '3.4', 'fancy_name' : 'nettle' },
}