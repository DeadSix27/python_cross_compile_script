{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: https://files.dyne.org/frei0r/
		{ 'url' : 'https://files.dyne.org/frei0r/frei0r-plugins-1.6.1.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'e0c24630961195d9bd65aa8d43732469e8248e8918faa942cfb881769d11515e' }, ], },
		{ 'url' : 'https://ftp.osuosl.org/pub/blfs/conglomeration/frei0r/frei0r-plugins-1.6.1.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'e0c24630961195d9bd65aa8d43732469e8248e8918faa942cfb881769d11515e' }, ], },
	],
	'conf_system' : 'cmake',
	'run_post_patch' : [ # runs commands post the patch process
		'sed -i.bak "s/find_package (Cairo)//g" CMakeLists.txt', #idk
	],
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DWITHOUT_OPENCV=YES',
	'_info' : { 'version' : '1.6.1', 'fancy_name' : 'frei0r-plugins' },
}