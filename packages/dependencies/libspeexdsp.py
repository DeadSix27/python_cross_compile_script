{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/speexdsp.git',
	'run_post_patch' : [ 'autoreconf -fiv', ],
	#'custom_cflag' : '-O3',
	'configure_options' : '{autoconf_prefix_options}',
	'_info' : { 'version' : None, 'fancy_name' : 'speexdsp' },
}