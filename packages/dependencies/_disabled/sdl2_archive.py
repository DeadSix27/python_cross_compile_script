{
	'repo_type' : 'archive',
	'url' : 'https://www.libsdl.org/release/SDL2-2.0.7.zip',
	# 'patches' : (
	# 	('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/sdl2/0001-SDL2-2.0.5.xinput.diff', '-p0'),
	# ),
	'custom_cflag' : '-DDECLSPEC=', # avoid SDL trac tickets 939 and 282, and not worried about optimizing yet...
	"run_post_install": (
		# 'sed -i.bak "s/-mwindows/-ldinput8 -ldxguid -ldxerr8 -luser32 -lgdi32 -lwinmm -limm32 -lole32 -loleaut32 -lshell32 -lversion -luuid/" "{pkg_config_path}/sdl2.pc"', # allow ffmpeg to output anything to console :|
		# 'sed -i.bak "s/-mwindows/-ldinput8 -ldxguid -ldxerr8 -luser32 -lgdi32 -lwinmm -limm32 -lole32 -loleaut32 -lshell32 -lversion -luuid/" "{target_prefix}/bin/sdl2-config"', # update this one too for good measure, FFmpeg can use either, not sure which one it defaults to...
		'cp -v "{target_prefix}/bin/sdl2-config" "{cross_prefix_full}sdl2-config"',
	),
	'configure_options': '--prefix={target_prefix} --host={target_host} --disable-shared --enable-static',
	'_info' : { 'version' : '2.0.7', 'fancy_name' : 'SDL2' },
}