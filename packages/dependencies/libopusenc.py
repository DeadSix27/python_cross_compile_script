{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/libopusenc.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'depends_on' : [
		'libopus',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'libopusenc' },
}