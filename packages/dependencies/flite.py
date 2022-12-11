{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'http://www.festvox.org/flite/packed/flite-2.0/flite-2.0.0-release.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '678c3860fd539402b5d1699b921239072af6acb4e72dc4720494112807cae411' }, ], },
		# { 'url' : 'http://www.speech.cs.cmu.edu/flite/packed/flite-1.4/flite-1.4-release.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '45c662160aeca6560589f78daf42ab62c6111dd4d244afc28118c4e6f553cd0c' }, ], },
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
	'_info' : { 'version' : '1.4', 'fancy_name' : 'flite' },
}