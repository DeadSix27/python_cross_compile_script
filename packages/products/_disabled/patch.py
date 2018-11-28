{
	'repo_type' : 'archive',
	'download_locations' : [
		{ "url" : "https://ftp.gnu.org/gnu/patch/patch-2.7.6.tar.xz", "hashes" : [ { "type" : "sha256", "sum" : "ac610bda97abe0d9f6b7c963255a11dcb196c25e337c61f94e4778d632f1d8fd" }, ], },
		{ "url" : "https://fossies.org/linux/misc/patch-2.7.6.tar.xz", "hashes" : [ { "type" : "sha256", "sum" : "ac610bda97abe0d9f6b7c963255a11dcb196c25e337c61f94e4778d632f1d8fd" }, ], },
	],
	'configure_options': '--host={target_host} --prefix={product_prefix}/patch.installed --disable-shared --enable-static',
	'_info' : { 'version' : '2.7.6', 'fancy_name' : 'patch' },
}