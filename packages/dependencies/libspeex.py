{
	'repo_type' : 'git', #"LDFLAGS=-lwinmm"
	'url' : 'https://github.com/xiph/speex.git',
	'configure_options' : '{autconf_prefix_options}',
	'depends_on' : [ 'libogg', 'libspeexdsp', ],
	'_info' : { 'version' : None, 'fancy_name' : 'speex' },
}