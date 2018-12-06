{
	'repo_type' : 'git',
	'url' : 'https://git.xiph.org/flac.git',
	'configure_options' : '--host={target_host} --prefix={product_prefix}/flac_git.installed --disable-shared --enable-static',
	'depends_on' : [
		'libogg',
	],
	'packages' : {
		'ubuntu' : [ 'docbook-to-man' ],
	},
	'_info' : { 'version' : None, 'fancy_name' : 'FLAC' },
}