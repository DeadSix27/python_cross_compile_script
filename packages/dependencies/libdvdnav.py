{
	'repo_type' : 'git',
	'url' : 'https://code.videolan.org/videolan/libdvdnav.git',
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --with-libdvdcss',
	'depends_on' : (
		'libdvdread',
	),
	'run_post_patch' : (
		'autoreconf -fiv',
	),
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libdvdnav' },
}