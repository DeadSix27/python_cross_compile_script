{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://www.quut.com/gsm/gsm-1.0.22.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'f0072e91f6bb85a878b2f6dbf4a0b7c850c4deb8049d554c65340b3bf69df0ac' }, ], },
	],
	'folder_name' : 'gsm-1.0-pl22',
	'patches' : [
		('gsm/gsm-1.0.16.patch', '-p0'),
		('gsm/gsm-1.0.16_Makefile.patch', '-p0'), # toast fails. so lets just patch it out of the makefile..
	],
	'needs_configure' : False,
	'needs_make_install' : False,
	'run_post_build' : [
		'cp -fv lib/libgsm.a {target_prefix}/lib',
		'mkdir -pv {target_prefix}/include/gsm',
		'cp -fv inc/gsm.h {target_prefix}/include/gsm',
	],
	#'cpu_count' : '1',
	'build_options' : '{make_prefix_options} INSTALL_ROOT={target_prefix}',
	'update_check' : { 'url' : 'http://www.quut.com/gsm', 'type' : 'httpregex', 'regex' : r'<a href="http:\/\/www.quut.com/gsm/gsm-(?P<version_num>[\d.]+)\.tar\.gz">sourcecode<\/a>' },
	'_info' : { 'version' : '1.0.22', 'fancy_name' : 'gsm' },
}