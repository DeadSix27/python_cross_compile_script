{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: http://fftw.org/download.html
		{ "url" : "http://fftw.org/fftw-3.3.8.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "6113262f6e92c5bd474f2875fa1b01054c4ad5040f6b0da7c03c98821d9ae303" }, ], },
		{ "url" : "https://fossies.org/linux/misc/fftw-3.3.8.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "6113262f6e92c5bd474f2875fa1b01054c4ad5040f6b0da7c03c98821d9ae303" }, ], },
	],
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'_info' : { 'version' : '3.3.8', 'fancy_name' : 'fftw3' },
}