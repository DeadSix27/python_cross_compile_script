{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: https://ftp.gnu.org/gnu/nettle/?C=M;O=D
		{ "url" : "https://ftp.gnu.org/gnu/nettle/nettle-3.4.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "ae7a42df026550b85daca8389b6a60ba6313b0567f374392e54918588a411e94" }, ], },
		{ "url" : "https://fossies.org/linux/privat/nettle-3.4.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "ae7a42df026550b85daca8389b6a60ba6313b0567f374392e54918588a411e94" }, ], },
	],
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-openssl --with-included-libtasn1',
	'depends_on' : [
		'gmp',
	],
	'_info' : { 'version' : '3.4', 'fancy_name' : 'nettle' },
}