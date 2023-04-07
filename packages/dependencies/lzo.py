{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'http://www.oberhumer.com/opensource/lzo/download/lzo-2.10.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'c0f892943208266f9b6543b3ae308fab6284c5c90e627931446fb49b4221a072' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/lzo-2.10.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'c0f892943208266f9b6543b3ae308fab6284c5c90e627931446fb49b4221a072' }, ], },
	],
	#'custom_cflag' : '-O3',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DENABLE_SHARED=0 -DCMAKE_BUILD_TYPE=Release',
	'update_check' : { 'url' : 'https://www.oberhumer.com/opensource/lzo/download/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'lzo-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '2.10', 'fancy_name' : 'lzo' },
}