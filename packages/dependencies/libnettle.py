{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://ftp.gnu.org/gnu/nettle/nettle-3.4.1.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'f941cf1535cd5d1819be5ccae5babef01f6db611f9b5a777bae9c7604b8a92ad' }, ], },
		{ 'url' : 'https://fossies.org/linux/privat/nettle-3.4.1.tar.gz/', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'f941cf1535cd5d1819be5ccae5babef01f6db611f9b5a777bae9c7604b8a92ad' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-openssl --with-included-libtasn1',
	'depends_on' : [
		'gmp',
	],
	'update_check' : { 'url' : 'https://ftp.gnu.org/gnu/nettle/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'nettle-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '3.4.1', 'fancy_name' : 'nettle' },
}