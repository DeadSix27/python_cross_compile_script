{
	'repo_type' : 'git',
	'url' : 'https://github.com/erikd/libsamplerate.git',
	'conf_system' : 'cmake',
	#'custom_cflag' : '-O3',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DLIBSAMPLERATE_EXAMPLES=OFF -DLIBSAMPLERATE_TESTS=OFF -DBUILD_SHARED_LIBS=0 -DCMAKE_BUILD_TYPE=Release',
	'depends_on' : ['libflac', 'fftw', 'libopus',],
	'_info' : { 'version' : None, 'fancy_name' : 'libsamplerate' },
}