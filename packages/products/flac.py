{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/flac.git',
	'configure_options' : '--host={target_host} --prefix={output_prefix}/flac_git.installed --disable-shared --enable-static',
	'custom_cflag' : '-O3 -D_FORTIFY_SOURCE=0',
	'depends_on' : [
		'libogg',
	],
	'packages' : {
		'ubuntu' : [ 'docbook-to-man' ],
	},
	'_info' : { 'version' : None, 'fancy_name' : 'FLAC' },
}