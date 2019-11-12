{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/opusfile.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'depends_on' : [
		'libressl', 'libopus'
	],
	'_info' : { 'version' : None, 'fancy_name' : 'opusfile' },
}