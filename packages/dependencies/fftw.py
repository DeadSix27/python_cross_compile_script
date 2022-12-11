{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'http://ftp.fftw.org/fftw-3.3.10.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '56c932549852cddcfafdab3820b0200c7742675be92179e59e6215b340e26467' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/fftw-3.3.10.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '56c932549852cddcfafdab3820b0200c7742675be92179e59e6215b340e26467' }, ], },
	],
	#'custom_cflag' : '-O3 -DWITH_OUR_MALLOC',
	'cflag_addition': '-DWITH_OUR_MALLOC',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DCMAKE_BUILD_TYPE=Release '
		'-DBUILD_TESTS=OFF '
		'-DENABLE_THREADS=ON '
		'-DENABLE_FLOAT=OFF '
		'-DENABLE_LONG_DOUBLE=OFF '
		'-DENABLE_QUAD_PRECISION=OFF '
		'-DENABLE_SSE=ON '
		'-DENABLE_SSE2=ON '
		'-DENABLE_AVX=ON '
		'-DENABLE_AVX2=ON '
	,
	'regex_replace': {
		'post_patch': [
			{
				0: r'fftw\${{PREC_SUFFIX}}\.pc',
				1: r'fftw3${{PREC_SUFFIX}}.pc',
				'in_file': '../CMakeLists.txt'
			},
		],
	},
	'update_check' : { 'url' : 'ftp://ftp.fftw.org/pub/fftw/', 'type' : 'ftpindex', 'regex' : r'fftw-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '3.3.10', 'fancy_name' : 'fftw' },
}