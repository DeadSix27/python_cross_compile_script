{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/speexdsp.git',
	'run_post_patch' : [ 'autoreconf -fiv', ],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'speexdsp' },
}