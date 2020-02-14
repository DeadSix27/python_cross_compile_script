{
	#export CC_FOR_BUILD=/usr/bin/gcc idk if we need this anymore, compiles fine without.
	#export CPP_FOR_BUILD=usr/bin/cpp
	#generic_configure "ABI=$bits_target"
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://gmplib.org/download/gmp/gmp-6.2.0.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '258e6cd51b3fbdfc185c716d55f82c08aff57df0c6fbd143cf6ed561267a1526' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/gmp-6.2.0.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '258e6cd51b3fbdfc185c716d55f82c08aff57df0c6fbd143cf6ed561267a1526' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'update_check' : { 'url' : 'https://gmplib.org/download/gmp/', 'type' : 'httpindex', 'regex' : r'gmp-(?P<version_num>[\d.]+)\.tar\.xz' },
	'_info' : { 'version' : '6.2.0', 'fancy_name' : 'gmp' },
}