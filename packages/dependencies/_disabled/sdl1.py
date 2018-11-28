{
	'repo_type' : 'archive',
	'url' : 'https://www.libsdl.org/release/SDL-1.2.15.tar.gz',
	'custom_cflag' : '-DDECLSPEC=',# avoid SDL trac tickets 939 and 282, and not worried about optimizing yet...
	"run_post_install": (
		'sed -i.bak "s/-mwindows//" "{pkg_config_path}/sdl.pc"', # allow ffmpeg to output anything to console :|
		'sed -i.bak "s/-mwindows//" "{target_prefix}/bin/sdl-config"', # update this one too for good measure, FFmpeg can use either, not sure which one it defaults to...
		'cp -v "{target_prefix}/bin/sdl-config" "{cross_prefix_full}sdl-config"', # this is the only mingw dir in the PATH so use it for now [though FFmpeg doesn't use it?]
	),
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'_info' : { 'version' : '1.2.15', 'fancy_name' : 'SDL1' },
}