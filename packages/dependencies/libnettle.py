{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://ftp.gnu.org/gnu/nettle/nettle-3.6.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'd24c0d0f2abffbc8f4f34dcf114b0f131ec3774895f3555922fe2f40f3d5e3f1' }, ], },
		{ 'url' : 'https://fossies.org/linux/privat/nettle-3.6.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'd24c0d0f2abffbc8f4f34dcf114b0f131ec3774895f3555922fe2f40f3d5e3f1' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-openssl --disable-mini-gmp',
	'depends_on' : [
		'gmp',
	],
	'update_check' : { 'url' : 'https://ftp.gnu.org/gnu/nettle/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'nettle-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '3.6', 'fancy_name' : 'nettle' },
}