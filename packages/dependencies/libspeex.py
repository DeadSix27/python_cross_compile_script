{
	'repo_type' : 'git', #"LDFLAGS=-lwinmm"
	'url' : 'https://github.com/xiph/speex.git',
	'configure_options' : '{autoconf_prefix_options}',
	#'custom_cflag' : '-O3',
	'depends_on' : [ 'libogg', 'libspeexdsp', ],
	'_info' : { 'version' : None, 'fancy_name' : 'speex' },
}