{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.15.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'ccf536620a45458d26ba83887a983b96827001e92a13847b45e4925cc8913178' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/libiconv-1.15.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'ccf536620a45458d26ba83887a983b96827001e92a13847b45e4925cc8913178' }, ], },
	],
	# CFLAGS=-O2
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-nls --enable-extra-encodings',
	'update_check_url' : { 'url' : 'https://ftp.gnu.org/pub/gnu/libiconv/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'libiconv-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '1.15', 'fancy_name' : 'libiconv' },
}