{
	'repo_type' : 'archive',
	'url' : 'https://bitbucket.org/mpyne/game-music-emu/downloads/game-music-emu-0.6.1.tar.bz2', # ffmpeg doesnt like git
	'conf_system' : 'cmake',
	#'run_post_patch': ( # runs commands post the patch process
	#	'sed -i.bak "s|SHARED|STATIC|" gme/CMakeLists.txt',
	#),
	'configure_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF',
	'_info' : { 'version' : '0.6.1', 'fancy_name' : 'game-music-emu' },
}