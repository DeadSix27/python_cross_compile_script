{
	'repo_type' : 'git',
	'url' : 'https://github.com/rocky/libcdio-paranoia.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	#'custom_cflag' : '-O3',
	'depends_on' : [
		'libcdio',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'libcdio-paranoia' },
}