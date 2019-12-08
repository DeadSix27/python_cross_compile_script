{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/opusfile.git',
	'depth_git': 0,
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'depends_on' : [
		'libressl', 'libopus', 'libogg'
	],
	'_info' : { 'version' : None, 'fancy_name' : 'opusfile' },
}