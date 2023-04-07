{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'http://www.festvox.org/flite/packed/flite-2.1/flite-2.1-release.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'c73c3f6a2ea764977d6eaf0a287722d1e2066b4697088c552e342c790f3d2b85' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/flite-2.1-release.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'c73c3f6a2ea764977d6eaf0a287722d1e2066b4697088c552e342c790f3d2b85' }, ], },
	],
	'patches' : [
		('flite/flite_64.diff', '-p0'),
	],
	'configure_options' : '{autoconf_prefix_options}',
	'cpu_count' : '1',
	'needs_make_install' : False,
	'regex_replace': {
		'post_patch': [
			{
				0: r'tools main',
				1: r'tools',
				'in_file': 'Makefile'
			}
		]
	},
    'do_not_git_update': True,
	'run_post_patch' : [
		'sed -i.bak "s|i386-mingw32-|{cross_prefix_bare}|" configure',
		'sed -i "s|-DWIN32 -shared|-DWIN64 -static|" configure',
	],
	'run_post_build' : [
		'mkdir -pv "{target_prefix}/include/flite"',
		'cp -fv include/* "{target_prefix}/include/flite"',
		'cp -fv ./build/{bit_name}-mingw32/lib/*.a "{target_prefix}/lib"',
	],
	# 'update_check' : { 'url' : 'http://www.speech.cs.cmu.edu/flite/packed/', 'type' : 'httpindex', 'regex' : r'flite-(?P<version_num>[\d.]+)\/' },
	'_info' : { 'version' : '2.1', 'fancy_name' : 'flite' },
}