{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: https://sourceforge.net/projects/opencore-amr/files/opencore-amr/
		{ 'url' : 'https://sourceforge.net/projects/opencore-amr/files/opencore-amr/opencore-amr-0.1.5.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '2c006cb9d5f651bfb5e60156dbff6af3c9d35c7bbcc9015308c0aff1e14cd341' }, ], },
		{ 'url' : 'https://sourceforge.mirrorservice.org/o/op/opencore-amr/opencore-amr/opencore-amr-0.1.5.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '2c006cb9d5f651bfb5e60156dbff6af3c9d35c7bbcc9015308c0aff1e14cd341' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'_info' : { 'version' : '0.1.5', 'fancy_name' : 'opencore-amr' },
}