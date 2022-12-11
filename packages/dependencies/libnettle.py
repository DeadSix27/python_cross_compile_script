{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://ftp.gnu.org/gnu/nettle/nettle-3.8.1.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '364f3e2b77cd7dcde83fd7c45219c834e54b0c75e428b6f894a23d12dd41cbfe' }, ], },
		{ 'url' : 'https://fossies.org/linux/privat/nettle-3.8.1.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '364f3e2b77cd7dcde83fd7c45219c834e54b0c75e428b6f894a23d12dd41cbfe' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-openssl --disable-mini-gmp',
	#'custom_cflag' : '-O3',
	'depends_on' : [
		'gmp',
	],
	'update_check' : { 'url' : 'https://ftp.gnu.org/gnu/nettle/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'nettle-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '3.8.1', 'fancy_name' : 'nettle' },
}