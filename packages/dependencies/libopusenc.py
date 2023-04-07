{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/libopusenc.git',
	'depth_git': 0,
	#'custom_cflag' : '-O3',
	'configure_options' : '{autoconf_prefix_options}',
	'depends_on' : [
		'libopus',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'libopusenc' },
}