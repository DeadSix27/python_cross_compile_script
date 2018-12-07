{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://sourceware.org/pub/libffi/libffi-3.2.1.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'd06ebb8e1d9a22d19e38d63fdb83954253f39bedc5d46232a05645685722ca37' }, ], },
		{ 'url' : 'https://www.mirrorservice.org/sites/sourceware.org/pub/libffi/libffi-3.2.1.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'd06ebb8e1d9a22d19e38d63fdb83954253f39bedc5d46232a05645685722ca37' }, ], },
	],
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-doc',
	'update_check' : { 'url' : 'https://sourceware.org/pub/libffi/', 'type' : 'httpindex', 'regex' : r'libffi-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '3.2.1', 'fancy_name' : 'libffi' },
}
