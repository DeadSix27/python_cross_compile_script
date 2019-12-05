{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://github.com/njh/twolame/releases/download/0.4.0/twolame-0.4.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'cc35424f6019a88c6f52570b63e1baf50f62963a3eac52a03a800bb070d7c87d' }, ], },
		{ 'url' : 'https://sourceforge.net/projects/twolame/files/twolame/0.4.0/twolame-0.4.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'cc35424f6019a88c6f52570b63e1baf50f62963a3eac52a03a800bb070d7c87d' }, ], },
	],
	'configure_options' : '{autconf_prefix_options}', #  CPPFLAGS=-DLIBTWOLAME_STATIC
	'update_check' : { 'url' : 'https://github.com/njh/twolame/releases/', 'type' : 'githubreleases', 'name_or_tag' : 'tag_name' },
	'_info' : { 'version' : '0.4.0', 'fancy_name' : 'twolame' },
}