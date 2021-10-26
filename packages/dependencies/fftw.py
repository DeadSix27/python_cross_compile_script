{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'http://ftp.fftw.org/fftw-3.3.9.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'bf2c7ce40b04ae811af714deb512510cc2c17b9ab9d6ddcf49fe4487eea7af3d' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/fftw-3.3.9.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'bf2c7ce40b04ae811af714deb512510cc2c17b9ab9d6ddcf49fe4487eea7af3d' }, ], },
	],
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
	'_info' : { 'version' : '3.3.9', 'fancy_name' : 'fftw' },
}