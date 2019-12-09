{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://files.dyne.org/frei0r/frei0r-plugins-1.7.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '1b1ff8f0f9bc23eed724e94e9a7c1d8f0244bfe33424bb4fe68e6460c088523a' }, ], },
		{ 'url' : 'https://cdn.netbsd.org/pub/pkgsrc/distfiles/frei0r-plugins-1.7.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '1b1ff8f0f9bc23eed724e94e9a7c1d8f0244bfe33424bb4fe68e6460c088523a' }, ], },
	],
	'depends_on' : [ 'dlfcn-win32', ],
	'conf_system' : 'cmake',
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DWITHOUT_OPENCV=YES',
	# 'run_post_patch' : [
	# 	'sed -i.bak "s/find_package (Cairo)//g" CMakeLists.txt',
	# ],
	'update_check' : { 'url' : 'https://files.dyne.org/frei0r/releases/', 'type' : 'httpindex', 'regex' : r'frei0r-plugins-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '1.7.0', 'fancy_name' : 'frei0r-plugins' },
}