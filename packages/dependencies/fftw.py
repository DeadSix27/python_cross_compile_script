{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'http://fftw.org/fftw-3.3.8.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '6113262f6e92c5bd474f2875fa1b01054c4ad5040f6b0da7c03c98821d9ae303' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/fftw-3.3.8.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '6113262f6e92c5bd474f2875fa1b01054c4ad5040f6b0da7c03c98821d9ae303' }, ], },
	],
	'cflag_addition': '-DWITH_OUR_MALLOC',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DCMAKE_BUILD_TYPE=Release '
		'-DBUILD_TESTS=OFF '
		'-DENABLE_THREADS=ON '
		'-DENABLE_FLOAT=ON '
		'-DENABLE_LONG_DOUBLE=OFF '
		'-DENABLE_QUAD_PRECISION=OFF '
		'-DENABLE_SSE=ON '
		'-DENABLE_SSE2=ON '
		'-DENABLE_AVX=ON '
		'-DENABLE_AVX2=ON '
	,
	'update_check' : { 'url' : 'ftp://ftp.fftw.org/pub/fftw/', 'type' : 'ftpindex', 'regex' : r'fftw-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '3.3.8', 'fancy_name' : 'fftw' },
}