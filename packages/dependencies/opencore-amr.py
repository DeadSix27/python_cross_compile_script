{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://sourceforge.net/projects/opencore-amr/files/opencore-amr/opencore-amr-0.1.6.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '483eb4061088e2b34b358e47540b5d495a96cd468e361050fae615b1809dc4a1' }, ], },
		{ 'url' : 'https://sourceforge.mirrorservice.org/o/op/opencore-amr/opencore-amr/opencore-amr-0.1.6.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '483eb4061088e2b34b358e47540b5d495a96cd468e361050fae615b1809dc4a1' }, ], },
	],
	'configure_options' : '{autoconf_prefix_options}',
	'update_check' : { 'url' : 'https://sourceforge.net/projects/opencore-amr/files/opencore-amr/', 'type' : 'sourceforge', 'regex' : r'opencore-amr-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '0.1.6', 'fancy_name' : 'opencore-amr' },
}