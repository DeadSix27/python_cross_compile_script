{
	'repo_type' : 'git',
	'url' : 'https://git.xiph.org/flac.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'custom_cflag' : '-O3 -D_FORTIFY_SOURCE=0',
	'depends_on' : [
		'libogg',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'flac (library)' },
}