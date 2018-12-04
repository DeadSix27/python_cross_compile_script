{
	'repo_type' : 'git',
	'url' : 'https://github.com/rocky/libcdio-paranoia.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'depends_on' : [
		'libcdio',
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libcdio-paranoia' },
}