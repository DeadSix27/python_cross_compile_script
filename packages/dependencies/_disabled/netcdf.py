{
	'repo_type' : 'archive',
	'download_locations' : [
		{ "url" : "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.6.1.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "89c7957458740b763ae828c345240b8a1d29c2c1fed0f065f99b73181b0b2642" }, ], },
		{ "url" : "https://fossies.org/linux/misc/netcdf-4.6.1.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "89c7957458740b763ae828c345240b8a1d29c2c1fed0f065f99b73181b0b2642" }, ], },
	],
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-netcdf-4 --disable-dap',
	'_info' : { 'version' : '4.6.1', 'fancy_name' : 'netcdf' },
}