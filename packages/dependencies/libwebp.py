{
	'repo_type' : 'git',
	'url' : 'https://chromium.googlesource.com/webm/libwebp',
	#'branch' : '082757087332f55c7daa5a869a19f1598d0be401', #old: e4eb458741f61a95679a44995c212b5f412cf5a1
	'run_post_patch' : [
		'sed -i.bak "s/\$LIBPNG_CONFIG /\$LIBPNG_CONFIG --static /g" configure.ac', # fix building with libpng
		'autoreconf -fiv',
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-swap-16bit-csp --enable-experimental --enable-libwebpmux --enable-libwebpdemux --enable-libwebpdecoder --enable-libwebpextras',
	'depends_on' : [ 'libpng', 'libjpeg-turbo' ],
	'_info' : { 'version' : None, 'fancy_name' : 'libwebp' },
}