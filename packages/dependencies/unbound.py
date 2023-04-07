{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://nlnetlabs.nl/downloads/unbound/unbound-1.17.1.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'ee4085cecce12584e600f3d814a28fa822dfaacec1f94c84bfd67f8a5571a5f4' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/unbound-1.17.1.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'ee4085cecce12584e600f3d814a28fa822dfaacec1f94c84bfd67f8a5571a5f4' }, ], },
	],
	'configure_options' :
		'--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-gost --disable-ecdsa'
	,
	'depends_on' : [
		# 'libressl',
	],
	'_info' : { 'version' : '1.17.1', 'fancy_name' : 'unbound' },
}