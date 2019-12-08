{
	'repo_type' : 'git',
	'do_not_bootstrap' : True,
	'run_post_patch' : [
		'autoreconf -fiv',
	],
	'patches' :	[
		( 'mfx/mfx-0001-mingwcompat-disable-va.patch', '-p1' ),
	],
	'url' : 'https://github.com/lu-zero/mfx_dispatch.git',
	'configure_options' : '{autoconf_prefix_options} --without-libva_drm --without-libva_x11',
	'_info' : { 'version' : None, 'fancy_name' : 'intel_quicksync_mfx' },
}