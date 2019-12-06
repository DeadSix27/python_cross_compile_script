{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'http://fftw.org/fftw-3.3.8.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '6113262f6e92c5bd474f2875fa1b01054c4ad5040f6b0da7c03c98821d9ae303' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/fftw-3.3.8.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '6113262f6e92c5bd474f2875fa1b01054c4ad5040f6b0da7c03c98821d9ae303' }, ], },
	],
	'configure_options' : '{autoconf_prefix_options}',
	'update_check' : { 'url' : 'ftp://ftp.fftw.org/pub/fftw/', 'type' : 'ftpindex', 'regex' : r'fftw-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '3.3.8', 'fancy_name' : 'fftw3' },
}