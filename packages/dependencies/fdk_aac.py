{
	'repo_type' : 'git',
	'run_post_patch' : [
		'autoreconf -fiv',
	],
	'url' : 'https://github.com/mstorsjo/fdk-aac.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'fdk-aac' },
}