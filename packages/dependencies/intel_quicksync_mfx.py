{
	'repo_type' : 'git',
	'do_not_bootstrap' : True,
	'run_post_patch': [
		'autoreconf -fiv',
	],
	'patches' :	[
		[ 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/mfx/mfx-0001-mingwcompat-disable-va.patch', '-p1' ],
	],
	'url' : 'https://github.com/lu-zero/mfx_dispatch.git',
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --without-libva_drm --without-libva_x11',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'intel_quicksync_mfx' },
}