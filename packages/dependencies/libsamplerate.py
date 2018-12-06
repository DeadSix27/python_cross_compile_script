{
	'repo_type' : 'git',
	#'branch' : '7dcc9bb727dae4e2010cdc6ef7cda101b05509a4',
	'url' : 'https://github.com/erikd/libsamplerate.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-alsa',
	'_info' : { 'version' : None, 'fancy_name' : 'libsamplerate' },
	'depends_on' : [
		'libflac',
		'fftw3',
	],
}