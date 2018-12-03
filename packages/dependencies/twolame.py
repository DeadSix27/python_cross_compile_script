{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: https://github.com/njh/twolame/releases/
		{ 'url' : 'https://github.com/njh/twolame/releases/download/0.3.13/twolame-0.3.13.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '98f332f48951f47f23f70fd0379463aff7d7fb26f07e1e24e42ddef22cc6112a' }, ], },
		{ 'url' : 'https://sourceforge.net/projects/twolame/files/twolame/0.3.13/twolame-0.3.13.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '98f332f48951f47f23f70fd0379463aff7d7fb26f07e1e24e42ddef22cc6112a' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static CPPFLAGS=-DLIBTWOLAME_STATIC',
	'_info' : { 'version' : '0.3.13', 'fancy_name' : 'twolame' },
}