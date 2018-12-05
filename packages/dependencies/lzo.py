{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'http://www.oberhumer.com/opensource/lzo/download/lzo-2.10.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'c0f892943208266f9b6543b3ae308fab6284c5c90e627931446fb49b4221a072' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/lzo-2.10.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'c0f892943208266f9b6543b3ae308fab6284c5c90e627931446fb49b4221a072' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'update_check_url' : { 'url' : 'https://www.oberhumer.com/opensource/lzo/download/?C=M;O=D', 'type' : 'httpindex', 'regex' : 'lzo-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '2.10', 'fancy_name' : 'lzo' },
}