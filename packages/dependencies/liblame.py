{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://sourceforge.net/projects/lame/files/lame/3.100/lame-3.100.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'ddfe36cab873794038ae2c1210557ad34857a4b6bdc515785d1da9e175b1da1e' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/lame-3.100.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'ddfe36cab873794038ae2c1210557ad34857a4b6bdc515785d1da9e175b1da1e' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-nasm --disable-frontend',
	'update_check' : { 'url' : 'https://sourceforge.net/projects/lame/files/lame/', 'type' : 'sourceforge', },
	'_info' : { 'version' : '3.100', 'fancy_name' : 'LAME (library)' },
}