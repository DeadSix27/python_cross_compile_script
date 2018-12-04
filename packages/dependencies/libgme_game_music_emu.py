{
	'repo_type' : 'git',
	'url' : 'https://bitbucket.org/mpyne/game-music-emu.git',
	'conf_system' : 'cmake',
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DENABLE_UBSAN=OFF',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'game-music-emu' },
}