{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://src.fedoraproject.org/repo/pkgs/gsm/gsm-1.0.19.tar.gz/sha512/f69b4bf2d918b118b5de90b8ab88fd026008ac7432f07b872b81fe52cdc781f605dca8eedcdaebc8beb974cef388496c618f92a41961c62057009964159f8392/gsm-1.0.19.tar.gz',
			'hashes' : [ { 'type' : 'sha256', 'sum' : '4903652f68a8c04d0041f0d19b1eb713ddcd2aa011c5e595b3b8bca2755270f6' }, ],
		},
		{ 'url' : 'http://www.quut.com/gsm/gsm-1.0.19.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '4903652f68a8c04d0041f0d19b1eb713ddcd2aa011c5e595b3b8bca2755270f6' }, ], },
	],
	'folder_name' : 'gsm-1.0-pl18',
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
	'_info' : { 'version' : '1.0.19', 'fancy_name' : 'gsm' },
}