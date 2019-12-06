{
	'repo_type' : 'git',
	'url' : 'https://github.com/erikd/libsamplerate.git',
	'configure_options' : '{autoconf_prefix_options} --disable-alsa',
	'depends_on' : [
		'libflac',
		'fftw',
		'libopus',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'libsamplerate' },
}