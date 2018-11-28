{
	'repo_type' : 'git',
	'url' : 'https://git.xiph.org/flac.git',
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'depends_on': [
		'libogg',
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'flac (library)' },
}