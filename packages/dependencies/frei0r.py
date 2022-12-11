{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://files.dyne.org/frei0r/frei0r-plugins-1.8.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '45a28655caf057227b442b800ca3899e93490515c81e212d219fdf4a7613f5c4' }, ], },
		{ 'url' : 'https://cdn.netbsd.org/pub/pkgsrc/distfiles/frei0r-plugins-1.8.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '45a28655caf057227b442b800ca3899e93490515c81e212d219fdf4a7613f5c4' }, ], },
	],
	'depends_on' : [ 'dlfcn-win32', ],
	'conf_system' : 'cmake',
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DWITHOUT_OPENCV=YES',
	# 'run_post_patch' : [
	# 	'sed -i.bak "s/find_package (Cairo)//g" CMakeLists.txt',
	# ],
	'update_check' : { 'url' : 'https://files.dyne.org/frei0r/releases/', 'type' : 'httpindex', 'regex' : r'frei0r-plugins-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '1.8.0', 'fancy_name' : 'frei0r-plugins' },
}