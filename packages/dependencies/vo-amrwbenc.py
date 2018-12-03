{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: https://sourceforge.net/projects/opencore-amr/files/vo-amrwbenc/
		{ 'url' : 'https://pkgs.rpmfusion.org/repo/pkgs/free/vo-amrwbenc/vo-amrwbenc-0.1.3.tar.gz/f63bb92bde0b1583cb3cb344c12922e0/vo-amrwbenc-0.1.3.tar.gz',
			'hashes' : [ { 'type' : 'sha256', 'sum' : '5652b391e0f0e296417b841b02987d3fd33e6c0af342c69542cbb016a71d9d4e'}, ],
		},
		{ 'url' : 'https://sourceforge.net/projects/opencore-amr/files/vo-amrwbenc/vo-amrwbenc-0.1.3.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '5652b391e0f0e296417b841b02987d3fd33e6c0af342c69542cbb016a71d9d4e' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'_info' : { 'version' : '0.1.3', 'fancy_name' : 'vo-amrwbenc' },
}