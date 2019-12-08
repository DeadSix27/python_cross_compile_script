{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://sourceforge.net/projects/opencore-amr/files/opencore-amr/opencore-amr-0.1.5.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '2c006cb9d5f651bfb5e60156dbff6af3c9d35c7bbcc9015308c0aff1e14cd341' }, ], },
		{ 'url' : 'https://sourceforge.mirrorservice.org/o/op/opencore-amr/opencore-amr/opencore-amr-0.1.5.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '2c006cb9d5f651bfb5e60156dbff6af3c9d35c7bbcc9015308c0aff1e14cd341' }, ], },
	],
	'configure_options' : '{autoconf_prefix_options}',
	'update_check' : { 'url' : 'https://sourceforge.net/projects/opencore-amr/files/opencore-amr/', 'type' : 'sourceforge', 'regex' : r'opencore-amr-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '0.1.5', 'fancy_name' : 'opencore-amr' },
}