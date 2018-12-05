{
	#export CC_FOR_BUILD=/usr/bin/gcc idk if we need this anymore, compiles fine without.
	#export CPP_FOR_BUILD=usr/bin/cpp
	#generic_configure "ABI=$bits_target"
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://gmplib.org/download/gmp/gmp-6.1.2.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '87b565e89a9a684fe4ebeeddb8399dce2599f9c9049854ca8c0dfbdea0e21912' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/gmp-6.1.2.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '87b565e89a9a684fe4ebeeddb8399dce2599f9c9049854ca8c0dfbdea0e21912' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'update_check_url' : { 'url' : 'https://gmplib.org/download/gmp/', 'type' : 'httpindex', 'regex' : 'gmp-(?P<version_num>[\d.]+)\.tar\.xz' },
	'_info' : { 'version' : '6.1.2', 'fancy_name' : 'gmp' },
}