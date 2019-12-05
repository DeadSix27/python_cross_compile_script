{
	'repo_type' : 'git',
	'url' : 'https://github.com/dekkers/libilbc.git',
	'run_post_patch' : [
		'autoreconf -fiv',
	],
	'configure_options' : '{autconf_prefix_options}',
	'_info' : { 'version' : None, 'fancy_name' : 'libilbc' },
}