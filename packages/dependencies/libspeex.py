{
	'repo_type' : 'git', #"LDFLAGS=-lwinmm"
	'url' : 'https://github.com/xiph/speex.git',
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'depends_on' : [ 'libogg', 'libspeexdsp', ],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'speex' },
}