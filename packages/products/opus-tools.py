{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/opus-tools',
	'custom_cflag' : '-O3 -D_FORTIFY_SOURCE=0',
	'configure_options' : '--host={target_host} --prefix={output_prefix}/opus-tools_git.installed --disable-shared --enable-static',
	'depends_on' : [
		'opusfile', 'libopusenc'
	],
	'_info' : { 'version' : None, 'fancy_name' : 'opus-tools' },
}