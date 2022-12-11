{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://nlnetlabs.nl/downloads/unbound/unbound-1.17.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'dcbc95d7891d9f910c66e4edc9f1f2fde4dea2eec18e3af9f75aed44a02f1341' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/unbound-1.17.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'dcbc95d7891d9f910c66e4edc9f1f2fde4dea2eec18e3af9f75aed44a02f1341' }, ], },
	],
	'configure_options' :
		'--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-gost --disable-ecdsa'
	,
	'depends_on' : [
		'libressl',
	],
	'_info' : { 'version' : '1.17.0', 'fancy_name' : 'unbound' },
}