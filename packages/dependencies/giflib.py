{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://sourceforge.net/projects/giflib/files/giflib-5.1.4.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'df27ec3ff24671f80b29e6ab1c4971059c14ac3db95406884fc26574631ba8d5' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/giflib-5.1.4.tar.bz2'				  , 'hashes' : [ { 'type' : 'sha256', 'sum' : 'df27ec3ff24671f80b29e6ab1c4971059c14ac3db95406884fc26574631ba8d5' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static', # I found no easy way to notbuild gifbuild.exe,etc..
	'update_check' : { 'url' : 'https://sourceforge.net/projects/giflib/files/', 'type' : 'sourceforge', 'regex' : r'giflib-(?P<version_num>[\d.]+)\.tar\.bz2' },
	'_info' : { 'version' : '5.1.4', 'fancy_name' : 'giflib' },
}