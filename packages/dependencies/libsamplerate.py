{
	'repo_type' : 'git',
	'url' : 'https://github.com/erikd/libsamplerate.git',
	'configure_options' : '{autconf_prefix_options} --disable-alsa',
	'depends_on' : [
		'libflac',
		'fftw3',
		'libopus',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'libsamplerate' },
}